from django.contrib import admin
from .models import Subject, SubjectStudent, SubjectCourse, SubjectSemester, SubjectYearLevel


class SubjectAdmin(admin.ModelAdmin):
    filter_horizontal = ['courses']


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectStudent)
admin.site.register(SubjectCourse)
admin.site.register(SubjectSemester)
admin.site.register(SubjectYearLevel)
