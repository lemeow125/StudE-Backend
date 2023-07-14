from rest_framework import serializers
from .models import StudyGroup, StudyGroupMembership
from accounts.models import CustomUser
from subjects.models import Subject
from drf_extra_fields.geo_fields import PointField


class StudyGroupSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), many=True, slug_field='name', required=False, allow_null=True)
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()

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
