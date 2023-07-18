from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from year_levels.models import Year_Level
from semesters.models import Semester
from courses.models import Course
from subjects.models import Subject


class CustomUserForm(forms.ModelForm):
    year_level = forms.ModelChoiceField(
        queryset=Year_Level.objects.all(), required=False)
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(), required=False)
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), required=False)
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('student_id_number',
         'year_level', 'semester', 'course', 'subjects', 'avatar', 'is_student', 'is_banned')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
