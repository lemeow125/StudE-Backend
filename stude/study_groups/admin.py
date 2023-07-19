from django.contrib import admin
from .models import StudyGroup, StudyGroupMembership
from leaflet.admin import LeafletGeoAdmin


admin.site.register(StudyGroup, LeafletGeoAdmin)
admin.site.register(StudyGroupMembership)
