from rest_framework import serializers
from .models import Message
from accounts.models import CustomUser
from study_groups.models import StudyGroup


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field='full_name', required=True)
    study_group = serializers.SlugRelatedField(
        queryset=StudyGroup.objects.all(), slug_field='name', required=True)

    class Meta:
        model = Message
        fields = '__all__'
