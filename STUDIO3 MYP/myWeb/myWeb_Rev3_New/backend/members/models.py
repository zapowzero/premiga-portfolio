# backend/members/models.py
from django.db import models

class Member(models.Model):
    bid = models.IntegerField(null=True, blank=True)  # CSV 'id' field, allow null/blank
    country = models.CharField(max_length=10, null=True, blank=True)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    classification = models.CharField(max_length=20, null=True, blank=True)
    imgProfile = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstName or ''} {self.lastName or ''}".strip() or str(self.pk)

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    sport = models.CharField(max_length=50, null=True, blank=True)
    players = models.ManyToManyField(Member, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.date})"