from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry
from django.db.models.signals import post_migrate
from django.dispatch import receiver
# Create your models here.


class Landmark(models.Model):
    name = models.CharField(max_length=64)
    location = gis_models.PolygonField()

    def __str__(self):
        return self.name


@receiver(post_migrate)
def populate_landmarks(sender, **kwargs):
    if sender.name == 'landmarks':
        SRID = 4326
        Landmark.objects.get_or_create(
            name='Gymnasium',
            location=GEOSGeometry(
                'POLYGON ((124.656383 8.485963, 124.656576 8.485483, 124.657009 8.485659, 124.656827 8.486126, 124.656383 8.485963))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Arts & Culture Building',
            location=GEOSGeometry(
                'POLYGON ((124.658427 8.486268, 124.658432 8.48617, 124.658582 8.486202, 124.658555 8.4863, 124.658427 8.486268))',
                srid=SRID
            )
        )
        # Add more predefined records as needed
