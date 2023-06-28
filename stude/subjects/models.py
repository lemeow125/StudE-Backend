from django.db import models
from year_levels.models import Year_Level
from semesters.models import Semester
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)
    courses = models.ManyToManyField(
        'courses.Course', through='courses.SubjectCourse', related_name='SubjectCourse_subject')
    students = models.ManyToManyField(
        'accounts.CustomUser', through='subjects.SubjectStudent', related_name='SubjectStudent_subject')

    year_level = models.ForeignKey(
        Year_Level,
        on_delete=models.SET_NULL,
        null=True,
        related_name='Year_Level_name'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name


class SubjectStudent(models.Model):
    user = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)

    def __str__(self):
        return f'User: User={self.user_id}, Subject={self.subject_name}'
