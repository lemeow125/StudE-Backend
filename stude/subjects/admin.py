from django.contrib import admin
from courses.models import Course
from .models import Subject, SubjectStudent


class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ['courses']


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectStudent)
