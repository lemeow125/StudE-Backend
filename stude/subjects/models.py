from django.db import models
from year_levels.models import Year_Level
from semesters.models import Semester
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)
    courses = models.ManyToManyField(
        'courses.Course', through='subjects.SubjectCourse', related_name='SubjectCourse_subject')
    students = models.ManyToManyField(
        'accounts.CustomUser', blank=True)

    year_levels = models.ManyToManyField(
        'year_levels.Year_Level', through='subjects.SubjectYearLevel', related_name='SubjectYearLevel_subject')

    semesters = models.ManyToManyField(
        'semesters.Semester', through='subjects.SubjectSemester', related_name='SubjectSemester_subject')

    def __str__(self):
        return self.name


class SubjectCourse(models.Model):
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Subject={self.subject.name}, Course={self.course.name}'

    class Meta:
        unique_together = [['subject', 'course']]


class SubjectYearLevel(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)
    year_level = models.ForeignKey(
        'year_levels.Year_Level', on_delete=models.CASCADE)

    def __str__(self):
        return f'Subject={self.subject.name}, Year Level={self.year_level.name}'

    class Meta:
        unique_together = [['subject', 'year_level']]


class SubjectSemester(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)
    semester = models.ForeignKey(
        'semesters.Semester', on_delete=models.CASCADE)

    def __str__(self):
        return f'Subject={self.subject.name}, Semester={self.semester.name}'

    class Meta:
        unique_together = [['subject', 'semester']]
