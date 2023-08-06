from rest_framework import serializers
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

    class Meta:
        model = StudentStatus
        fields = '__all__'
        read_only_fields = ['user', 'landmark']

    def create(self, validated_data):
        user = self.context['request'].user
        student_status = StudentStatus.objects.create(
            user=user, defaults=validated_data)
        return student_status

    def update(self, instance, validated_data):
        active = validated_data.get('active', None)
        subject = validated_data.get('subject', None)

        # If status is set as inactive or if no subject is specified in the request, clear the student status
        if active is not None and active is False or not subject:
            validated_data['location'] = Point(0, 0)
            validated_data['subject'] = None
            validated_data['landmark'] = None
        else:
            # Check each landmark to see if our location is within it
            for landmark in Landmark.objects.all():
                if landmark.location.contains(validated_data['location']):
                    validated_data['landmark'] = landmark
                    break

        return super().update(instance, validated_data)
