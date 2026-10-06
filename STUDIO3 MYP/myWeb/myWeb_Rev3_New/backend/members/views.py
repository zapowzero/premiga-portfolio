from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from .models import Member, Event
from datetime import date

# ------------------------------
# Member CRUD + Search
# ------------------------------
def member_list(request):
    members = Member.objects.order_by('bid', 'id')
    page_obj = Paginator(members, 25).get_page(request.GET.get('page'))
    return render(request, 'members/member_list.html', {
        'members': page_obj,
        'page_obj': page_obj,
        'total': members.count(),
    })

def member_search(request):
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'name')
    results = Member.objects.none()

    if query:
        if search_type == 'id':
            results = Member.objects.filter(bid=int(query)) if query.isdigit() else Member.objects.none()

        elif search_type == 'name':
            # Every word must appear in the first or last name, so "chai", "sok"
            # and "chaiya sok" all find Chaiya SOK.
            results = Member.objects.all()
            for word in query.split():
                results = results.filter(Q(firstName__icontains=word) | Q(lastName__icontains=word))

        elif search_type == 'country':
            results = Member.objects.filter(country__icontains=query)

        elif search_type == 'classification':
            results = Member.objects.filter(classification__icontains=query)

        elif search_type == 'gender':
            aliases = {'male': 'Men', 'man': 'Men', 'men': 'Men',
                       'female': 'Women', 'woman': 'Women', 'women': 'Women'}
            results = Member.objects.filter(gender__iexact=aliases.get(query.lower(), query))

        results = results.order_by('bid', 'id')

    return render(request, 'members/search.html', {
        'results': results,
        'query': query,
        'search_type': search_type
    })


# ------------------------------
# MemberForm (modern design)
# ------------------------------
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'bid': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Member ID'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Country'
            }),
            'firstName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'lastName': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'dateOfBirth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': '1900-01-01',
}
            ),
            'classification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. T46',
            }),
            'imgProfile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paste image URL here',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
            }),
        }
        labels = {'bid': 'Member ID', 'firstName': 'First name', 'lastName': 'Last name',
                  'dateOfBirth': 'Date of birth', 'imgProfile': 'Profile image URL'}

    # Same values as the athlete data in the CSV ("Men" / "Women")
    GENDER_CHOICES = [('', '---------'), ('Men', 'Men'), ('Women', 'Women')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = list(self.GENDER_CHOICES)
        current = getattr(self.instance, 'gender', None)
        if current and current not in dict(choices):
            choices.append((current, current))  # never silently change an existing value
        self.fields['gender'].widget.choices = choices

@login_required
def member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    form.fields['dateOfBirth'].widget.attrs['max'] = date.today().isoformat()
    return render(request, 'members/member_form.html', {'form': form})

@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    form.fields['dateOfBirth'].widget.attrs['max'] = date.today().isoformat()
    return render(request, 'members/member_form.html', {'form': form, 'member': member})

@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': member})

# ------------------------------
# Event CRUD (modern style)
# ------------------------------
class EventForm(forms.ModelForm):
    time_start = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    time_end = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    sport = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sport name'})
    )
    players = forms.ModelMultipleChoiceField(
        queryset=Member.objects.order_by('firstName', 'lastName'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Event
        fields = ['name', 'date', 'time_start', 'time_end', 'location', 'sport', 'players', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event name'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter details...'}),
        }


def event_list(request):
    events = Event.objects.order_by('date', 'time_start')
    return render(request, 'members/event_list.html', {'events': events})

@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # also saves players, so removing every player works too
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'members/event_form.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()  # also saves players, so removing every player works too
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'members/event_form.html', {'form': form, 'event': event})


def event_detail(request, pk):
    """แสดงหน้ารายละเอียดของกิจกรรมที่เลือก"""
    event = get_object_or_404(Event, pk=pk)
    players = event.players.all()
    
    context = {
        'event': event,
        'players': players,
    }
    
    return render(request, 'members/event_detail.html', context)

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'members/event_confirm_delete.html', {'event': event})


def faq_view(request):
    return render(request, 'members/faq_page.html')