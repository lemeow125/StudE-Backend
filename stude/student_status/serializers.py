from rest_framework import serializers, exceptions
from .models import StudentStatus
from subjects.models import Subject
from django.contrib.gis.geos import Point
from drf_extra_fields.geo_fields import PointField
from landmarks.models import Landmark
from study_groups.models import StudyGroup


class StudentStatusSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', required=True, many=False)
    user = serializers.CharField(source='user.full_name', read_only=True)
    location = PointField(required=True)
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)

    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    active = serializers.BooleanField(required=True)
    study_group = serializers.SlugRelatedField(queryset=StudyGroup.objects.all(
    ), many=False, slug_field='name', required=False, allow_null=True)

    class Meta:
        model = StudentStatus
        fields = ['user', 'subject', 'location',
                  'timestamp', 'active', 'study_group', 'landmark']
        read_only_fields = ['user', 'landmark']

    def create(self, validated_data):
        user = self.context['request'].user
        student_status = StudentStatus.objects.create(
            user=user, defaults=validated_data)
        return student_status

    def update(self, instance, validated_data):

        active = validated_data.get('active', None)
        # If status is set as false in PATCH, clear the student status
        if active is False:
            validated_data['location'] = Point(0, 0)
            validated_data['subject'] = None
            validated_data['landmark'] = None
            validated_data['study_group'] = None
        # If status is set as true in PATCH
        elif active is True:
            # Check if subject is attached in PATCH, if not return error
            if 'subject' not in validated_data:
                raise serializers.ValidationError(
                    {'subject': 'This field may not be empty if active is true'})
            # Then check the location if it matches any landmarks
            for landmark in Landmark.objects.all():
                if landmark.location.contains(validated_data['location']):
                    validated_data['landmark'] = landmark
                    break

        # Get new value for study group in PATCH
        study_group = validated_data.get('study_group', None)
        # Get old value in db
        old_study_group = instance.study_group

        # Commit changes
        instance = super().update(instance, validated_data)

        # If student has left study group, check if the old study_group no longer has any students
        if study_group is None and old_study_group is not None:
            if not old_study_group.students.exists():
                # If there are no students left in the old StudyGroup, delete it
                old_study_group.delete()

        return instance


class StudentStatusLocationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', required=True)
    location = PointField(required=True)
    distance = serializers.SerializerMethodField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)
    study_group = serializers.SlugRelatedField(queryset=StudyGroup.objects.all(
    ), many=False, slug_field='name', required=False, allow_null=True)

    class Meta:
        model = StudentStatus
        fields = ['user', 'location', 'distance',
                  'subject', 'active', 'study_group', 'landmark']
        read_only_fields = ['user', 'distance', 'subject',
                            'active', 'study_group', 'landmark']

    def get_distance(self, obj):
        return obj.distance.km

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['distance'] = self.get_distance(instance)
        return representation
