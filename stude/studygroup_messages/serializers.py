from rest_framework import serializers
from .models import Message
from accounts.models import CustomUser


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field='full_name')
    group = serializers.CharField(source='subject.Subject', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
