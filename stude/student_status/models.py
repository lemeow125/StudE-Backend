from django.db import models
from accounts.models import CustomUser
from study_groups.models import StudyGroup
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
# Create your models here.


class StudentStatus(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    location = gis_models.PointField(blank=True, null=True)
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    study_group = models.ManyToManyField(
        'study_groups.StudyGroup', through='study_groups.StudyGroupMembership', blank=True)

    def __str__(self):
        return self.user.full_name
