from rest_framework import serializers
from .models import Subject, SubjectInstance, SubjectCode
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class SubjectInstanceSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(
        queryset=SubjectCode.objects.all(), slug_field='name', allow_null=False)
    code = serializers.SlugRelatedField(
        queryset=SubjectCode.objects.all(), slug_field='code', allow_null=False)
    year_level = serializers.SlugRelatedField(
        queryset=Year_Level.objects.all(), slug_field='name', allow_null=True)
    semester = serializers.SlugRelatedField(
        queryset=Semester.objects.all(), slug_field='name', allow_null=True)
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(), slug_field='name', allow_null=True)

    class Meta:
        model = SubjectInstance
        fields = ('id', 'subject', 'code', 'course', 'year_level', 'semester')
