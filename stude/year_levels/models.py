from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.


class Year_Level(models.Model):
    name = models.CharField(max_length=64, unique=True)
    shortname = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


@receiver(post_migrate)
def populate_courses(sender, **kwargs):
    if sender.name == 'year_levels':
        Year_Level.objects.get_or_create(
            name='1st Year', shortname='1stYr')
        Year_Level.objects.get_or_create(
            name='2nd Year', shortname='2ndYr')
        Year_Level.objects.get_or_create(
            name='3rd Year', shortname='3rdYr')
        Year_Level.objects.get_or_create(
            name='4th Year', shortname='4thYr')
        # Year_Level.objects.get_or_create(
        # name='Irregular', shortname='Irreg')
        # Add more predefined records as needed
