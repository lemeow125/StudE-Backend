from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Landmark

admin.site.register(Landmark, LeafletGeoAdmin)
