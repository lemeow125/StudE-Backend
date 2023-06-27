from rest_framework import serializers
from .models import Subject
from year_levels.serializers import YearLevelSerializer
from semesters.serializers import SemesterSerializer


class SubjectSerializer(serializers.ModelSerializer):
    year_level = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_year_level(self, obj):
        return obj.year_level.name

    def get_semester(self, obj):
        return obj.semester.name
