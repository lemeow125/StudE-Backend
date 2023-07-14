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
        Landmark.objects.get_or_create(
            name='Guidance and Testing Center',
            location=GEOSGeometry(
                'POLYGON ((124.658191 8.486326, 124.658377 8.486359, 124.658394 8.486261, 124.658209 8.486231, 124.658191 8.486326))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Old Civil Engineering Building',
            location=GEOSGeometry(
                'POLYGON ((124.657244 8.485617, 124.657228 8.485743, 124.658014 8.485844, 124.658032 8.485711, 124.657244 8.485617))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='ITB Building',
            location=GEOSGeometry(
                'POLYGON ((124.658035 8.48622, 124.658056 8.485906, 124.658592 8.485942, 124.658582 8.486077, 124.6582 8.486056, 124.658188 8.486231, 124.658035 8.48622))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='SPED Center',
            location=GEOSGeometry(
                'POLYGON ((124.658236 8.485918, 124.658348 8.485923, 124.658348 8.485874, 124.658236 8.485881, 124.658236 8.485918))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Administration Building',
            location=GEOSGeometry(
                'POLYGON ((124.657236 8.486097, 124.657213 8.486064, 124.657196 8.486074, 124.657177 8.486037, 124.657279 8.485944, 124.657401 8.485893, 124.657426 8.485935, 124.657411 8.485946, 124.65743 8.485971, 124.657236 8.486097))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Informations and Communications Technology Building',
            location=GEOSGeometry(
                'POLYGON ((124.657204 8.486478, 124.657142 8.486326, 124.657201 8.486307, 124.657273 8.486272, 124.657291 8.486287, 124.65741 8.486216, 124.65752 8.486097, 124.657552 8.486031, 124.657537 8.486025, 124.657523 8.486009, 124.657513 8.485994, 124.657512 8.485978, 124.657515 8.48596, 124.657521 8.485944, 124.657535 8.485927, 124.65756 8.485914, 124.657578 8.48591, 124.657592 8.485913, 124.65761 8.485921, 124.657627 8.485934, 124.657639 8.485948, 124.657639 8.485963, 124.657639 8.485978, 124.657638 8.485992, 124.657626 8.486008, 124.657605 8.486025, 124.657666 8.486053, 124.657634 8.486139, 124.65758 8.486206, 124.657511 8.486279, 124.657425 8.486352, 124.65735 8.486405, 124.657204 8.486478))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Finance and Accounting Building',
            location=GEOSGeometry(
                'POLYGON ((124.656457 8.486273, 124.656844 8.486425, 124.656974 8.486104, 124.656855 8.486057, 124.656772 8.486259, 124.656503 8.486157, 124.656457 8.486273))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Culinary Building',
            location=GEOSGeometry(
                'POLYGON ((124.65708 8.485527, 124.657104 8.485261, 124.657205 8.485268, 124.657175 8.485533, 124.65708 8.485527))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Science Centrum Building',
            location=GEOSGeometry(
                'POLYGON ((124.657114 8.485195, 124.657128 8.484964, 124.657224 8.48497, 124.657212 8.485202, 124.657114 8.485195))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Engineering Complex Right Wing',
            location=GEOSGeometry(
                'POLYGON ((124.656961 8.484943, 124.656934 8.48482, 124.656959 8.484813, 124.656939 8.484744, 124.657229 8.484684, 124.657228 8.484898, 124.656961 8.484943))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Engineering Complex Left Wing',
            location=GEOSGeometry(
                'POLYGON ((124.656949 8.484975, 124.656962 8.484944, 124.656935 8.484821, 124.656701 8.484767, 124.65666 8.484765, 124.656632 8.484772, 124.656605 8.484783, 124.656596 8.484798, 124.656591 8.484813, 124.656588 8.484828, 124.656587 8.484858, 124.656595 8.484878, 124.656604 8.484893, 124.65662 8.484907, 124.656647 8.484922, 124.656681 8.484935, 124.656693 8.484903, 124.656949 8.484975))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Cafeteria',
            location=GEOSGeometry(
                'POLYGON ((124.656651 8.48535, 124.656772 8.485021, 124.656917 8.485077, 124.656799 8.485403, 124.656651 8.48535))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='HRM Building',
            location=GEOSGeometry(
                'POLYGON ((124.656359 8.486151, 124.656471 8.486198, 124.656497 8.486141, 124.656627 8.486189, 124.656655 8.486118, 124.65641 8.486023, 124.656359 8.486151))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Sports Complex',
            location=GEOSGeometry(
                'POLYGON ((124.65625 8.486543, 124.656813 8.486763, 124.65687 8.486617, 124.656306 8.486401, 124.65625 8.486543))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Printing Press',
            location=GEOSGeometry(
                'POLYGON ((124.656053 8.486711, 124.656092 8.486597, 124.656195 8.486636, 124.656152 8.486748, 124.656053 8.486711))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Learning Resource Center',
            location=GEOSGeometry(
                'POLYGON ((124.655575 8.486698, 124.655663 8.486454, 124.655783 8.486502, 124.655799 8.486458, 124.655916 8.486499, 124.655899 8.486543, 124.656041 8.486593, 124.655951 8.486833, 124.655575 8.486698))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Food Innovation Center',
            location=GEOSGeometry(
                'POLYGON ((124.655633 8.486304, 124.655681 8.486175, 124.656239 8.486394, 124.65619 8.486516, 124.656101 8.486482, 124.656085 8.486523, 124.656007 8.486494, 124.656022 8.486454, 124.655633 8.486304))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Technology Building',
            location=GEOSGeometry(
                'POLYGON ((124.655184 8.486766, 124.655252 8.486674, 124.655632 8.486823, 124.655575 8.486919, 124.655184 8.486766))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Foods Trade Building',
            location=GEOSGeometry(
                'POLYGON ((124.655251 8.486585, 124.655427 8.486651, 124.655478 8.486521, 124.655416 8.4865, 124.65552 8.486246, 124.655571 8.486263, 124.65563 8.486128, 124.655451 8.486059, 124.655251 8.486585))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Old Medical Building',
            location=GEOSGeometry(
                'POLYGON ((124.655574 8.485952, 124.655708 8.486004, 124.655732 8.485944, 124.655594 8.485895, 124.655574 8.485952))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Old Science Building',
            location=GEOSGeometry(
                'POLYGON ((124.655534 8.485857, 124.655629 8.485588, 124.655795 8.485647, 124.655755 8.485757, 124.656271 8.485946, 124.656212 8.486104, 124.655534 8.485857))',
                srid=SRID
            )
        ) 
        Landmark.objects.get_or_create(
            name='Science Complex',
            location=GEOSGeometry(
                'POLYGON ((124.655743 8.485616, 124.655743 8.48563, 124.655829 8.485659, 124.655845 8.485623, 124.656325 8.485793, 124.656381 8.485629, 124.655806 8.485427, 124.655761 8.485558, 124.655742 8.485547, 124.655719 8.485608, 124.655743 8.485616))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='SUMP PIT',
            location=GEOSGeometry(
                'POLYGON ((124.65478 8.486829, 124.654976 8.486897, 124.65502 8.486779, 124.654826 8.486707, 124.65478 8.486829))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Fabrication Laboratory',
            location=GEOSGeometry(
                'POLYGON ((124.654816 8.486586, 124.654933 8.4863, 124.65511 8.486373, 124.654993 8.486658, 124.654816 8.486586))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Old Student Center',
            location=GEOSGeometry(
                'POLYGON ((124.655046 8.486251, 124.655178 8.485921, 124.655311 8.485972, 124.655173 8.486301, 124.655046 8.486251))',
                srid=SRID
            )
        )
        Landmark.objects.get_or_create(
            name='Old Education Building',
            location=GEOSGeometry(
                'POLYGON ((124.655181 8.485909, 124.655307 8.485612, 124.655432 8.485663, 124.655305 8.485959, 124.655181 8.485909))',
                srid=SRID
            )
        )

        # Add more predefined records as needed
