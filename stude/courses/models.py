from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=64)
    shortname = models.CharField(max_length=16)

    def __str__(self):
        return self.shortname


@receiver(post_migrate)
def populate_courses(sender, **kwargs):
    if sender.name == 'courses':
        Course.objects.get_or_create(
            name='Bachelor of Science in Information Technology', shortname='BSIT')
        Course.objects.get_or_create(
            name='Bachelor of Science in Computer Science', shortname='BSCS')
        Course.objects.get_or_create(
            name='Bachelor of Science in Computer Engineering ', shortname='BSCpE')
        Course.objects.get_or_create(
            name='Bachelor of Science in Data Science', shortname='BSDS')
        # Add more predefined records as needed
