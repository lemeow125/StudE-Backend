from rest_framework import serializers
from .models import Message
from accounts.models import CustomUser
from study_groups.models import StudyGroup


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field='username', required=False)
    study_group = serializers.SlugRelatedField(
        queryset=StudyGroup.objects.all(), slug_field='name', required=False)
    message_content = serializers.CharField()
    timestamp = serializers.DateTimeField(format="%I:%M %p", required=False)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['user', 'study_group', 'timestamp']
