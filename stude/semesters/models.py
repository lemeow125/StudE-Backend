from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.


class Semester(models.Model):
    name = models.CharField(max_length=64)
    shortname = models.CharField(max_length=16)

    def __str__(self):
        return self.name


@receiver(post_migrate)
def populate_courses(sender, **kwargs):
    if sender.name == 'semesters':
        Semester.objects.get_or_create(
            name='1st Semester', shortname='1st')
        Semester.objects.get_or_create(
            name='2nd Semester', shortname='2nd')
        # Add more predefined records as needed
