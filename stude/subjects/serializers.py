from rest_framework import serializers
from .models import Subject
from courses.models import Course
from year_levels.serializers import YearLevelSerializer
from semesters.serializers import SemesterSerializer
from courses.serializers import CourseSerializer


class SubjectSerializer(serializers.ModelSerializer):
    year_level = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    courses = serializers.SlugRelatedField(
        queryset=Course.objects.all(), many=True, slug_field='name', allow_null=True)

    class Meta:
        model = Subject
        fields = ('name', 'code', 'courses', 'year_level', 'semester')

    def get_year_level(self, obj):
        return obj.year_level.name

    def get_semester(self, obj):
        return obj.semester.name
