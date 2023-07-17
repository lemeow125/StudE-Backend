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
        'accounts.CustomUser', through='subjects.SubjectStudent', related_name='SubjectStudent_subject')

    year_levels = models.ManyToManyField(
        'year_levels.Year_Level', through='subjects.SubjectYearLevel', related_name='SubjectYearLevel_subject')

    semesters = models.ManyToManyField(
        'semesters.Semester', through='subjects.SubjectSemester', related_name='SubjectSemester_subject')

    def __str__(self):
        return self.name


class SubjectStudent(models.Model):
    user = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)

    def __str__(self):
        return f'User={self.user_id}, Subject={self.subject_name}'


class SubjectCourse(models.Model):
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Subject={self.subject.name}, Course={self.course.name}'


class SubjectYearLevel(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)
    year_level = models.ForeignKey(
        'year_levels.Year_Level', on_delete=models.CASCADE)

    def __str__(self):
        return f'Subject={self.subject.name}, Year Level={self.year_level.name}'


class SubjectSemester(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE)
    semester = models.ForeignKey(
        'semesters.Semester', on_delete=models.CASCADE)

    def __str__(self):
        return f'Subject={self.subject.name}, Semester={self.semester.name}'
