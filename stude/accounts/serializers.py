from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions
from rest_framework import serializers
from accounts.models import CustomUser
from student_status.serializers import StudentStatusSerializer
from student_status.models import StudentStatus
from rest_framework.settings import api_settings
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(BaseUserSerializer):
    user_status = StudentStatusSerializer(
        source='studentstatus', read_only=True)
    course = serializers.StringRelatedField()
    year_level = serializers.StringRelatedField()
    semester = serializers.StringRelatedField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email',
                  'student_id_number', 'year_level', 'semester', 'course', 'subjects', 'avatar', 'first_name', 'last_name', 'is_banned', 'user_status')
        read_only_fields = ('is_banned', 'user_status')

# The model from your custom user


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    student_id_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser    # Use your custom user model here
        fields = ('username', 'email', 'password', 'student_id_number',
                  'year_level', 'semester', 'course', 'subjects', 'avatar',
                  'first_name', 'last_name')

    def validate(self, attrs):
        user = self.Meta.model(**attrs)
        password = attrs.get("password")
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        StudentStatus.objects.create(
            user=user,
            active=False,
            x=None,
            y=None,
            subject=None
        )
        return user
