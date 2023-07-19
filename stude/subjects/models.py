
import os
import csv
from django.conf import settings
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=64, unique=True)
    codes = models.ManyToManyField(
        'subjects.SubjectCode')
    courses = models.ManyToManyField(
        'courses.Course', through='subjects.SubjectCourse', related_name='SubjectCourse_subject')
    students = models.ManyToManyField(
        'accounts.CustomUser', blank=True)

    year_levels = models.ManyToManyField(
        'year_levels.Year_Level', through='subjects.SubjectYearLevel', related_name='SubjectYearLevel_subject')

    semesters = models.ManyToManyField(
        'semesters.Semester', through='subjects.SubjectSemester', related_name='SubjectSemester_subject')

    def __str__(self):
        code_list = ', '.join(self.codes.values_list('code', flat=True))
        return f'{self.name} ({code_list})'


class SubjectCode(models.Model):
    code = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.code


class SubjectCourse(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, to_field='name')
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, null=True, to_field='name')

    def __str__(self):
        return f'Subject={self.subject.name}, Course={self.course.name}'

    class Meta:
        unique_together = [['subject', 'course']]


class SubjectYearLevel(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, to_field='name')
    year_level = models.ForeignKey(
        'year_levels.Year_Level', on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return f'Subject={self.subject.name}, Year Level={self.year_level.name}'

    class Meta:
        unique_together = [['subject', 'year_level']]


class SubjectSemester(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, to_field='name')
    semester = models.ForeignKey(
        'semesters.Semester', on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return f'Subject={self.subject.name}, Semester={self.semester.name}'

    class Meta:
        unique_together = [['subject', 'semester']]


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
            print('Reading subjects from', filename)
            with open(csv_file_path, newline='') as csvfile:

                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                subject_count = 0
                for row in reader:
                    if not any(row):
                        continue

                    # Get subject information
                    year_term = row[0].split('-')
                    subject_year_level = year_term[0].strip()
                    subject_semester = year_term[1].strip()
                    subject_code = row[1]
                    subject_name = row[2]

                    ignored_subject_codes = ['NSTP', 'ROTC', 'CWTS', 'LTS']
                    ignored_subject_names = [
                        'PRACTICUM', 'On the Job Training', 'CAPSTONE', 'Capstone']
                    # Skip ignored subjects
                    if any(ignored_code in subject_code for ignored_code in ignored_subject_codes):
                        print('Ignored subject', subject_name,
                              'with code', subject_code)
                        continue

                    if any(ignored_name in subject_name for ignored_name in ignored_subject_names):
                        print('Ignored subject', subject_name,
                              'with code', subject_code)
                        continue

                    course = Course.objects.filter(
                        name=filename).first()
                    year_level = Year_Level.objects.filter(
                        name=subject_year_level).first()
                    semester = Semester.objects.filter(
                        name=subject_semester).first()
                    # Create the subject instance or get if it already exists
                    if (Subject.objects.filter(name=subject_name).exists()):
                        print('Updating existing subject',
                              subject_name, subject_code)
                        SUBJECT = Subject.objects.filter(name=subject_name
                                                         ).first()
                        SUBJECT.courses.add(course)
                        SUBJECT.year_levels.add(year_level)
                        SUBJECT.semesters.add(semester)
                        SUBJECT_CODE = SubjectCode.objects.get_or_create(
                            code=subject_code)
                        SUBJECT.codes.add(SUBJECT_CODE[0])
                    else:

                        SUBJECT = Subject.objects.get_or_create(
                            name=subject_name,
                        )
                        SUBJECT[0].courses.set([course])
                        SUBJECT[0].year_levels.set([year_level])
                        SUBJECT[0].semesters.set([semester])
                        SUBJECT_CODE = SubjectCode.objects.get_or_create(
                            code=subject_code)
                        SUBJECT[0].codes.add(SUBJECT_CODE[0])
                        subject_count += 1

                    # Set the course, year level, and semester of the subject
                print('Added', subject_count, 'subjects from', filename)
