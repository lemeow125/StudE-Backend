from rest_framework import serializers
from .models import Subject, SubjectInstance
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester


class SubjectInstanceSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='subject', read_only=True)
    year_level = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', allow_null=False)
    year_level = serializers.SlugRelatedField(
        queryset=Year_Level.objects.all(), slug_field='name', allow_null=True)
    semester = serializers.SlugRelatedField(
        queryset=Semester.objects.all(), slug_field='name', allow_null=True)
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = SubjectInstance
        fields = ('id', 'name', 'code',
                  'course', 'year_level', 'semester')
