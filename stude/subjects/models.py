from django.db import models
from year_levels.models import Year_Level
from semesters.models import Semester
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)
    courses = models.ManyToManyField(
        'courses.Course', through='courses.SubjectCourse', related_name='SubjectCourse_subject')

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
