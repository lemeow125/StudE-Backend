from rest_framework import serializers
from .models import Subject, SubjectCode
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester
from accounts.models import CustomUser


class SubjectSerializer(serializers.ModelSerializer):
    year_levels = serializers.SlugRelatedField(
        queryset=Year_Level.objects.all(), many=True, slug_field='name', allow_null=True)
    semesters = serializers.SlugRelatedField(
        queryset=Semester.objects.all(), many=True, slug_field='name', allow_null=True)
    courses = serializers.SlugRelatedField(
        queryset=Course.objects.all(), many=True, slug_field='name', allow_null=True)
    codes = serializers.SlugRelatedField(
        queryset=SubjectCode.objects.all(), many=True, slug_field='code', allow_null=False)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'codes', 'courses', 'year_levels', 'semesters')
