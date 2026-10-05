# backend/members/management/commands/import_members.py

import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from members.models import Member

class Command(BaseCommand):
    help = 'Import members from Athlests.member.csv'

    def handle(self, *args, **options):
        def none_if_empty(v):
            if v is None:
                return None
            v = v.strip()
            return v or None

        with open('members/Athlests.member.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                dob = none_if_empty(row.get('dateOfBirth'))
                dob_date = None
                if dob:
                    try:
                        dob_date = datetime.strptime(dob, '%d/%m/%Y').date()
                    except Exception:
                        dob_date = None
                Member.objects.create(
                    bid=int(row['id']) if row.get('id') else None,
                    country=none_if_empty(row.get('country')),
                    firstName=none_if_empty(row.get('firstName')),
                    lastName=none_if_empty(row.get('lastName')),
                    gender=none_if_empty(row.get('gender')),
                    dateOfBirth=dob_date,
                    classification=none_if_empty(row.get('classification')),
                    imgProfile=none_if_empty(row.get('imgProfile')),
                    email=none_if_empty(row.get('email')),
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {count} members.'))
