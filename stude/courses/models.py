import os
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import models
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=64, unique=True)
    shortname = models.CharField(max_length=16, unique=True)
    subjects = models.ManyToManyField(
        'subjects.Subject', related_name='SubjectCourse_course', through='subjects.SubjectCourse')

    def __str__(self):
        return self.name


'''
# Old Subject migration code
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
'''


# Create subjects based on records that we have
@receiver(post_migrate)
def populate_subjects(sender, **kwargs):
    if sender.name == 'courses':
        root_path = os.path.join(settings.MEDIA_ROOT, 'records')
        csv_files = [f for f in os.listdir(root_path) if f.endswith('.csv')]
        added_courses = 0
        existing_courses = 0
        print('Adding courses\n')
        for csv_file in csv_files:
            # The filename contains coursename
            filename = os.path.splitext(csv_file)[0]
            # Splitting the filename and constructing the shortname
            shortname = ''
            for word in filename.split(' '):
                if word[0].isupper():
                    shortname += word[0]

            if shortname != None:
                # If course already exists with relevant info, skip over it
                if (Course.objects.filter(name=filename, shortname=shortname).exists()):

                    existing_courses += 1
                    continue

                # Else add the course
                else:
                    Course.objects.get_or_create(
                        name=filename, shortname=shortname)
                    added_courses += 1

        print('Added', added_courses, 'courses')
        print(existing_courses, 'existing courses skipped\n')
