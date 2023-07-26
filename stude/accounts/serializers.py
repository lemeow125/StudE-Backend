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
from courses.models import Course
from year_levels.models import Year_Level
from semesters.models import Semester
from subjects.models import Subject
from django.contrib.gis.geos import Point
from django.utils.encoding import smart_str
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

# There can be multiple subject instances with the same name, only differing in course, year level, and semester. We filter them here


class SubjectSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        user_course = self.context['request'].user.course
        try:
            subject = Subject.objects.get(name=data, course=user_course)
            return subject
        except Subject.DoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field,
                      value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class CustomUserSerializer(BaseUserSerializer):
    course_shortname = serializers.SerializerMethodField()
    yearlevel_shortname = serializers.SerializerMethodField()
    semester_shortname = serializers.SerializerMethodField()
    course = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Course.objects.all(), required=False, allow_null=True)
    year_level = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Year_Level.objects.all(), required=False, allow_null=True)
    semester = serializers.SlugRelatedField(
        many=False, slug_field='name', queryset=Semester.objects.all(), required=False, allow_null=True)
    # Use custom slug field for filtering
    subjects = SubjectSlugRelatedField(
        many=True, slug_field='name', queryset=Subject.objects.all(), required=False)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email',
                  'student_id_number', 'year_level', 'yearlevel_shortname', 'semester', 'semester_shortname', 'course', 'course_shortname', 'subjects', 'avatar', 'first_name', 'last_name', 'irregular')
        read_only_fields = ('user_status', 'yearlevel_shortname',
                            'semester_shortname', 'course_shortname')

    @extend_schema_field(OpenApiTypes.STR)
    def get_course_shortname(self, instance):
        return instance.course.shortname if instance.course else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_yearlevel_shortname(self, instance):
        return instance.year_level.shortname if instance.year_level else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_semester_shortname(self, instance):
        return instance.semester.shortname if instance.semester else None

    def update(self, instance, validated_data):
        # First, we'll remove all the existing subjects from the user
        print(validated_data)
        # If course, year_level, or semester is changed
        if any(field in validated_data for field in ['course', 'year_level', 'semester']):
            if (
                    instance.course is not validated_data['course'] or
                    instance.year_level is not validated_data['year_level'] or
                    instance.semester is not validated_data['semester'] or
                    instance.irregular is not validated_data['irregular']):

                # Clear all subjects
                instance.subjects.clear()
                # Update the user instance with the validated data
                instance = super().update(instance, validated_data)
                # Then add new subjects matching the new criteria
                self.add_subjects(instance)

            # This is what I want you to do. This comment below! Ignore any other comments
            #  Add another condition here to check if the user recently changed his/her irregular field from true to false. And if it has changed to false from being true, run the same if statement above

        else:
            # Else update as usual
            super().update(instance, validated_data)
        return instance

    def add_subjects(self, instance):
        # Get the matching subjects based on the user's course, year level, and semester
        matching_subjects = Subject.objects.filter(
            course=instance.course, year_level=instance.year_level, semester=instance.semester)
        # Add the matching subjects to the user's subjects list
        instance.subjects.add(*matching_subjects)

# The model from your custom user


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    student_id_number = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
    subjects = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=Subject.objects.all(), required=False, allow_null=True)

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
            location=Point(0, 0),
            subject=None
        )
        return user
