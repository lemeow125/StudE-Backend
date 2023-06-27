from django.db import models
from accounts.models import CustomUser
from study_groups.models import StudyGroup

# Create your models here.


class StudentStatus(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    study_group = models.ForeignKey(
        StudyGroup, on_delete=models.SET_NULL, null=True)
