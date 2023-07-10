from django.db import models
from django.contrib.gis.db import models as gis_models
# Create your models here.


class Landmark(models.Model):
    name = models.CharField(max_length=64)
    location = gis_models.PolygonField()

    def __str__(self):
        return self.name
