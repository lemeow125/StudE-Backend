from rest_framework import serializers
from .models import StudyGroup
from accounts.models import CustomUser
from subjects.models import Subject
from drf_extra_fields.geo_fields import PointField
from landmarks.models import Landmark
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer as BaseUserSerializer


class CustomUserAvatarSerializer(BaseUserSerializer):
    avatar = Base64ImageField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['avatar', 'username']


class CustomUserKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        # returns the string representation of the custom user (aka the name)
        return str(value)


class StudyGroupDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    students = serializers.StringRelatedField(many=True)
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ['landmark', 'radius', 'students', 'distance']


class StudyGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    students = serializers.StringRelatedField(many=True)
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)
    radius = serializers.FloatField()

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ['landmark', 'radius', 'students', 'distance']


class StudyGroupDistanceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    students = serializers.StringRelatedField(many=True)
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)
    distance = serializers.SerializerMethodField(default=0)

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ['landmark', 'radius', 'students', 'distance']

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return obj.distance.km
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['distance'] = self.get_distance(instance)
        representation['radius'] = 15
        return representation


class FullNameSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, instance):
        return instance.full_name


class StudyGroupCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    subject = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Subject.objects.all(), required=True, allow_null=False)
    location = PointField()
    landmark = serializers.SlugRelatedField(
        queryset=Landmark.objects.all(), many=False, slug_field='name', required=False, allow_null=True)

    def create(self, validated_data):
        user = self.context['request'].user
        study_group = StudyGroup.objects.create(
            name=validated_data['name'], location=validated_data['location'], subject=validated_data['subject'])
        for landmark in Landmark.objects.all():
            if landmark.location.contains(validated_data['location']):
                validated_data['landmark'] = landmark
                study_group.landmark = landmark
                study_group.save()
                break
        validated_data['location'].read_only = True
        return study_group

    def update(self, instance, validated_data):
        # Check each landmark to see if our location is within it
        if ('location' in validated_data):
            for landmark in Landmark.objects.all():
                if landmark.location.contains(validated_data['location']):
                    validated_data['landmark'] = landmark
                    break
        return super().update(instance, validated_data)

    class Meta:
        model = StudyGroup
        fields = '__all__'
        read_only_fields = ['landmark']
