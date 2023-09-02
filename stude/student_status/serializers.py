from rest_framework import serializers, exceptions
from .models import StudentStatus
from subjects.models import Subject
from django.contrib.gis.geos import Point
from drf_extra_fields.geo_fields import PointField
from landmarks.models import Landmark


class StudentStatusSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', required=True)
    user = serializers.CharField(source='user.full_name', read_only=True)
    location = PointField(required=True)
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)

    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    active = serializers.BooleanField(required=True)

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
        # subject = validated_data.get('subject', None)

        # If status is set as false in the request, clear the student status
        if active is False:
            validated_data['location'] = Point(0, 0)
            validated_data['subject'] = None
            validated_data['landmark'] = None
            validated_data['study_group'] = []
        else:
            if 'subject' not in validated_data:
                raise serializers.ValidationError(
                    {'subject': 'This field may not be empty if active is true'})
            # To-do: Add geofencing to ensure locations are always within USTP
            # Check each landmark to see if our location is within it
            for landmark in Landmark.objects.all():
                if landmark.location.contains(validated_data['location']):
                    validated_data['landmark'] = landmark
                    break

        return super().update(instance, validated_data)


class StudentStatusLocationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', required=True)
    location = PointField(required=True)
    distance = serializers.SerializerMethodField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)

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
