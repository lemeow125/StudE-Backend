from rest_framework import serializers
from .models import StudentStatus
from subjects.models import Subject
from django.contrib.gis.geos import Point


class StudentStatusSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(), slug_field='name', required=True)
    user = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = StudentStatus
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        student_status = StudentStatus.objects.create(
            user=user, defaults=validated_data)
        return student_status

    def update(self, instance, validated_data):
        active = validated_data.get('active', None)

        if active is not None and active is False:
            validated_data['location'] = Point(0, 0)
            validated_data['subject'] = None

        return super().update(instance, validated_data)
