from rest_framework import serializers
from .models import Subject
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester


class SubjectSerializer(serializers.ModelSerializer):
    year_level = serializers.SlugRelatedField(
        queryset=Year_Level.objects.all(), slug_field='name', allow_null=True)
    semester = serializers.SlugRelatedField(
        queryset=Semester.objects.all(), slug_field='name', allow_null=True)
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'code', 'course', 'year_level', 'semester')
