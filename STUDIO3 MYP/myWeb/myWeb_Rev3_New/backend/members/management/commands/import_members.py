# backend/members/management/commands/import_members.py
"""
Import athletes from Athlests.member.csv.

Safe to run more than once: each athlete is matched by CSV id + first name +
last name, so running it again updates the existing row instead of adding a
copy. (The CSV gives two different athletes the id 805, so the id alone is
not unique.)
It also merges duplicate rows left by earlier imports, moving their event
registrations onto the row that is kept.
"""
import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count

from members.models import Member, Event

CSV_PATH = Path(__file__).resolve().parents[2] / 'Athlests.member.csv'

GENDER_FIX = {'male': 'Men', 'men': 'Men', 'female': 'Women', 'women': 'Women'}


def none_if_empty(v):
    if v is None:
        return None
    v = v.strip()
    return v or None


def normalise_gender(v):
    v = none_if_empty(v)
    return GENDER_FIX.get(v.lower(), v) if v else None


class Command(BaseCommand):
    help = 'Import members from Athlests.member.csv (safe to run again)'

    @transaction.atomic
    def handle(self, *args, **options):
        merged = self.merge_duplicates()

        created = updated = 0
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if not none_if_empty(row.get('id')):
                    continue
                dob = none_if_empty(row.get('dateOfBirth'))
                try:
                    dob_date = datetime.strptime(dob, '%d/%m/%Y').date() if dob else None
                except ValueError:
                    dob_date = None

                _, was_created = Member.objects.update_or_create(
                    bid=int(row['id']),
                    firstName=none_if_empty(row.get('firstName')),
                    lastName=none_if_empty(row.get('lastName')),
                    defaults={
                        'country': none_if_empty(row.get('country')),
                        'gender': normalise_gender(row.get('gender')),
                        'dateOfBirth': dob_date,
                        'classification': none_if_empty(row.get('classification')),
                        'imgProfile': none_if_empty(row.get('imgProfile')),
                        'email': none_if_empty(row.get('email')),
                    },
                )
                created += was_created
                updated += not was_created

        # Tidy genders on athletes added by hand (e.g. "Female" -> "Women")
        for m in Member.objects.exclude(gender__isnull=True):
            fixed = normalise_gender(m.gender)
            if fixed != m.gender:
                m.gender = fixed
                m.save(update_fields=['gender'])

        self.stdout.write(self.style.SUCCESS(
            f'Merged {merged} duplicate rows. Created {created}, updated {updated}. '
            f'Total athletes: {Member.objects.count()}.'
        ))

    def merge_duplicates(self):
        """Keep the oldest row for each athlete, move event links onto it, delete the rest."""
        removed = 0
        groups = (Member.objects.exclude(bid__isnull=True)
                  .values('bid', 'firstName', 'lastName')
                  .annotate(n=Count('id')).filter(n__gt=1))
        for g in list(groups):
            rows = list(Member.objects.filter(bid=g['bid'], firstName=g['firstName'],
                                              lastName=g['lastName']).order_by('id'))
            keep, extras = rows[0], rows[1:]
            for extra in extras:
                for event in Event.objects.filter(players=extra):
                    event.players.add(keep)
                extra.delete()
                removed += 1
        return removed