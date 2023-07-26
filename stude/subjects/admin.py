from django.contrib import admin
from .models import Subject, SubjectCode, SubjectInstance

admin.site.register(Subject)
admin.site.register(SubjectInstance)
admin.site.register(SubjectCode)
