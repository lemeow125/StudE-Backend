
import os
import csv
from django.conf import settings
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from courses.models import Course
from accounts.models import CustomUser
from year_levels.models import Year_Level
from semesters.models import Semester


class Subject(models.Model):
    name = models.CharField(max_length=64)
    students = models.ManyToManyField(
        CustomUser, blank=True)
    code = models.CharField(max_length=16)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)
    year_level = models.ForeignKey(
        Year_Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'course', 'year_level', 'semester']

    def __str__(self):
        return f'Subject: {self.name}({self.code}) - {self.course.shortname} - {self.year_level} - {self.semester}'
# Create subjects on initial migrate


@receiver(post_migrate)
def populate_subjects(sender, **kwargs):
    if sender.name == 'subjects':
        root_path = os.path.join(settings.MEDIA_ROOT, 'records')
        csv_files = [f for f in os.listdir(root_path) if f.endswith('.csv')]

        for csv_file in csv_files:
            csv_file_path = os.path.join(root_path, csv_file)
            # Filename contains course of subjects
            filename = os.path.splitext(csv_file)[0]
            print('---', 'Adding Subjects from', filename, '---')
            with open(csv_file_path, newline='') as csvfile:

                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                subject_count = 0
                ignored_subjects = 0
                existing_subjects = 0
                for row in reader:
                    if not any(row):
                        continue

                    # Get subject information
                    year_term = row[0].split('-')
                    subject_year_level = year_term[0].strip()
                    subject_semester = year_term[1].strip()
                    subject_code = row[1]
                    subject_name = row[2].replace("\n", " ").replace("\r", "")

                    # Definitions of subjects to ignore
                    ignored_subject_codes = ['NSTP', 'ROTC', 'CWTS', 'LTS']
                    ignored_subject_names = [
                        'PRACTICUM', 'On the Job Training', 'CAPSTONE', 'Capstone']

                    # Skip ignored subjects
                    if any(ignored_code in subject_code for ignored_code in ignored_subject_codes):
                        ignored_subjects += 1
                        continue

                    if any(ignored_name in subject_name for ignored_name in ignored_subject_names):
                        ignored_subjects += 1
                        continue

                    # Get relevant info for specific subject
                    course = Course.objects.filter(
                        name=filename).first()
                    year_level = Year_Level.objects.filter(
                        name=subject_year_level).first()
                    semester = Semester.objects.filter(
                        name=subject_semester).first()

                    # If subject exists, skip over
                    if (Subject.objects.filter(name=subject_name, course=course, year_level=year_level, semester=semester, code=subject_code).exists()):
                        # print('Duplicate subject')
                        existing_subjects += 1
                        continue

                    # If subject does not exist at all, then create new subject
                    else:

                        SUBJECT, created = Subject.objects.get_or_create(
                            name=subject_name, course=course, year_level=year_level, semester=semester, code=subject_code)
                        subject_count += 1

                    # Set the course, year level, and semester of the subject
                print('Skipped', existing_subjects,
                      'already existing subjects')
                print('Added', subject_count, 'subjects')
                print('Ignored', ignored_subjects,
                      'subjects', '\n')
