from rest_framework import serializers
from .models import StudyGroup
from accounts.models import CustomUser
from subjects.models import Subject
from drf_extra_fields.geo_fields import PointField
from landmarks.models import Landmark


class CustomUserKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        # returns the string representation of the custom user (aka the name)
        return str(value)


class StudyGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    students = serializers.StringRelatedField(many=True)
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)
    radius = serializers.FloatField()

    def create(self, validated_data):
        user = self.context['request'].user
        study_group = StudyGroup.objects.create(
            users=[user], defaults=validated_data)
        validated_data['location'].read_only = True
        return study_group

    def update(self, instance, validated_data):
        # Check each landmark to see if our location is within it
        for landmark in Landmark.objects.all():
            if landmark.location.contains(validated_data['location']):
                validated_data['landmark'] = landmark
                break
        return super().update(instance, validated_data)

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ['landmark', 'radius', 'students']
