from django.db import models
from subjects.models import Subject
# Create your models here.


class StudyGroup(models.Model):
    name = models.CharField(max_length=48)
    users = models.ManyToManyField(
        'student_status.StudentStatus', through='StudyGroupMembership')
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)


class StudyGroupMembership(models.Model):
    user = models.ForeignKey(
        'student_status.StudentStatus', on_delete=models.CASCADE)
    study_group = models.ForeignKey(
        'study_groups.StudyGroup', on_delete=models.CASCADE)

    def __str__(self):
        return f'StudyGroupMembership: User={self.user_id}, StudyGroup={self.study_group_id}'
