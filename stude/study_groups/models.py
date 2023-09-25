from django.db import models
from subjects.models import Subject
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
# Create your models here.


class StudyGroup(models.Model):
    name = models.CharField(max_length=48)
    location = gis_models.PointField(blank=True, null=True, srid=4326)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    landmark = models.ForeignKey(
        'landmarks.Landmark', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
