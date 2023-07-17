from rest_framework import serializers
from .models import Subject
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester
from year_levels.serializers import YearLevelSerializer
from semesters.serializers import SemesterSerializer
from courses.serializers import CourseSerializer


class SubjectSerializer(serializers.ModelSerializer):
    year_levels = serializers.SlugRelatedField(
        queryset=Year_Level.objects.all(), many=True, slug_field='name', allow_null=True)
    semesters = serializers.SlugRelatedField(
        queryset=Semester.objects.all(), many=True, slug_field='name', allow_null=True)
    courses = serializers.SlugRelatedField(
        queryset=Course.objects.all(), many=True, slug_field='name', allow_null=True)

    class Meta:
        model = Subject
        fields = ('name', 'code', 'courses', 'year_levels', 'semesters')

    def get_year_level(self, obj):
        return obj.year_level.name

    def get_semester(self, obj):
        return obj.semester.name
