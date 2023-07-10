from django.contrib import admin
from .models import StudentStatus
from leaflet.admin import LeafletGeoAdmin

admin.site.register(StudentStatus, LeafletGeoAdmin)
