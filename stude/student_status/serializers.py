from rest_framework import serializers
from .models import StudentStatus


class StudentStatusSerializer(serializers.ModelSerializer):
    year_level = serializers.CharField(
        source='user.year_level', read_only=True)
    course = serializers.CharField(source='user.course', read_only=True)
    semester = serializers.CharField(source='user.semester', read_only=True)
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
            validated_data['x'] = None
            validated_data['y'] = None
            validated_data['subject'] = None

        return super().update(instance, validated_data)
