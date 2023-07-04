from rest_framework import serializers
from .models import StudyGroup, StudyGroupMembership
from accounts.models import CustomUser


class StudyGroupSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), many=True, slug_field='name', allow_null=True)
    subject = serializers.CharField(source='subject.Subject', read_only=True)

    class Meta:
        model = StudyGroup
        fields = '__all__'


class StudyGroupMembershipSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='accounts.CustomUser', read_only=True)
    subject = serializers.CharField(
        source='study_groups.StudyGroup', read_only=True)

    class Meta:
        model = StudyGroupMembership
        fields = '__all__'