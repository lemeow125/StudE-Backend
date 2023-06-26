from rest_framework import serializers
from .models import StudentStatus


class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        student_status, created = StudentStatus.objects.update_or_create(
            user=user, defaults=validated_data)
        return student_status
