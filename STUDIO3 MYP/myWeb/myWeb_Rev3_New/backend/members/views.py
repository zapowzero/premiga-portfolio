from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Member, Event
from datetime import date

# ------------------------------
# Member CRUD + Search
# ------------------------------
def member_list(request):
    members = Member.objects.all()
    return render(request, 'members/member_list.html', {'members': members})

from django.db.models import Q

def member_search(request):
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'name')
    results = []
    seen = set()

    if query:
        q = query.strip()
        
        if search_type == 'id':
            if q.isdigit():
                results = Member.objects.filter(bid__exact=int(q))
            else:
                results = []

        elif search_type == 'name':
            results = Member.objects.filter(
                Q(firstName__iexact=q) | Q(lastName__iexact=q)
                )

        elif search_type == 'country':
            results = Member.objects.filter(country__icontains=q)

        elif search_type == 'classification':
            results = Member.objects.filter(classification__icontains=q)

        elif search_type == 'gender':
            q_lower = q.lower().strip()
            results = Member.objects.filter(
                Q(gender__iexact=q_lower) |
                Q(gender__istartswith=f"All {q_lower.capitalize()}")
            )

        # Remove duplicates safely
        unique_results = []
        for m in results:
            key = (m.bid or m.id, m.firstName or '', m.lastName or '')
            if key not in seen:
                unique_results.append(m)
                seen.add(key)
        results = unique_results

    return render(request, 'members/search.html', {
        'results': results or [],
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
            'gender': forms.Select(
                choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
                attrs={'class': 'form-select'}
            ),
            'dateOfBirth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': '1900-01-01',
                    'max': date.today().strftime('%Y-%m-%d'),}
            ),
            'classification': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

@login_required
def member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
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
        queryset=Member.objects.all(),
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
    events = Event.objects.all()
    return render(request, 'members/event_list.html', {'events': events})

@login_required
def event_add(request):
    members = Member.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # แมพค่าจาก POST ไปที่ฟิลด์ในโมเดล
            event.time_start = request.POST.get('time_start') if request.POST.get('time_start') else None
            event.time_end = request.POST.get('time_end') if request.POST.get('time_end') else None
            event.sport = request.POST.get('sport') if request.POST.get('sport') else None
            event.save()
            if form.cleaned_data.get('players'):
                event.players.set(form.cleaned_data['players'])
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'members/event_form.html', {'form': form, 'members': members})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    members = Member.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            # แมพค่าจาก POST ไปที่ฟิตในโมเดล
            event.time_start = request.POST.get('time_start') if request.POST.get('time_start') else None
            event.time_end = request.POST.get('time_end') if request.POST.get('time_end') else None
            event.sport = request.POST.get('sport') if request.POST.get('sport') else None
            event.save()
            if form.cleaned_data.get('players'):
                event.players.set(form.cleaned_data['players'])
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'members/event_form.html', {'form': form, 'members': members, 'event': event})


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