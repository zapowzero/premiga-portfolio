from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Event, Member
from .views import MemberForm


class MemberTests(TestCase):
    def setUp(self):
        self.athlete = Member.objects.create(bid=103, firstName='Chaiya', lastName='SOK',
                                             gender='Women', country='CAM', classification='T46')
        User.objects.create_user('staff', password='Staff12345!')

    def test_login_required_pages_redirect_to_login_page(self):
        response = self.client.get(reverse('member_add'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('member_add')}")

    def test_name_search_matches_part_of_name_and_full_name(self):
        for q in ('chai', 'sok', 'Chaiya SOK'):
            response = self.client.get(reverse('member_search'), {'q': q, 'type': 'name'})
            self.assertEqual(list(response.context['results']), [self.athlete], q)

    def test_gender_search_accepts_female(self):
        response = self.client.get(reverse('member_search'), {'q': 'female', 'type': 'gender'})
        self.assertEqual(list(response.context['results']), [self.athlete])

    def test_edit_form_keeps_existing_gender(self):
        form = MemberForm(instance=self.athlete)
        self.assertIn('value="Women" selected', str(form['gender']))

    def test_member_list_is_paginated(self):
        Member.objects.bulk_create([Member(bid=i, firstName=f'A{i}') for i in range(1, 40)])
        response = self.client.get(reverse('member_list'))
        self.assertEqual(len(response.context['members']), 25)
        self.assertEqual(response.context['total'], 40)


class EventTests(TestCase):
    def test_can_remove_every_player_from_event(self):
        User.objects.create_user('staff', password='Staff12345!')
        self.client.login(username='staff', password='Staff12345!')
        player = Member.objects.create(bid=1, firstName='A')
        event = Event.objects.create(name='Final', date='2026-01-01', location='KKU')
        event.players.add(player)

        self.client.post(reverse('event_edit', args=[event.pk]),
                         {'name': 'Final', 'date': '2026-01-01', 'location': 'KKU'})
        self.assertEqual(event.players.count(), 0)


class ImportTests(TestCase):
    def test_import_twice_does_not_duplicate(self):
        call_command('import_members')
        first = Member.objects.count()
        call_command('import_members')
        self.assertEqual(Member.objects.count(), first)
        self.assertEqual(first, 100)  # 100 rows in the CSV (two athletes share id 805)

    def test_import_merges_old_duplicates_and_keeps_event_players(self):
        keep = Member.objects.create(bid=103, firstName='Chaiya', lastName='SOK')
        copy = Member.objects.create(bid=103, firstName='Chaiya', lastName='SOK')
        event = Event.objects.create(name='Final', date='2026-01-01', location='KKU')
        event.players.add(copy)

        call_command('import_members')

        self.assertEqual(Member.objects.filter(bid=103).count(), 1)
        self.assertEqual(list(event.players.all()), [keep])