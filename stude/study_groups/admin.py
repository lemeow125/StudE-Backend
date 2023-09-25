from django.contrib import admin
from .models import StudyGroup
from leaflet.admin import LeafletGeoAdmin


admin.site.register(StudyGroup, LeafletGeoAdmin)
