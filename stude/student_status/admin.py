from django.contrib import admin
from .models import StudentStatus
from leaflet.admin import LeafletGeoAdmin


class StudentStatusAdmin(LeafletGeoAdmin):
    # define which fields are required
    def get_form(self, request, obj=None, **kwargs):
        form = super(StudentStatusAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['landmark'].required = False
        return form


# Register the new StudentStatus model
admin.site.register(StudentStatus, StudentStatusAdmin)
