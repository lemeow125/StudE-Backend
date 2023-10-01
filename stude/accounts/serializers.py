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
from subjects.models import Subject, SubjectInstance
from django.contrib.gis.geos import Point
from django.utils.encoding import smart_str
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from drf_extra_fields.fields import Base64ImageField

# There can be multiple subject instances with the same name, only differing in course, year level, and semester. We filter them here


class SubjectSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return value.subject.name

    def to_internal_value(self, data):
        user_course = self.context['request'].user.course
        try:
            subject = SubjectInstance.objects.get(
                subject__name=data, course=user_course)
            return subject
        except SubjectInstance.DoesNotExist:
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
        many=True, slug_field='subject', queryset=SubjectInstance.objects.all(), required=False)
    avatar = Base64ImageField()

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
        # If irregular is updated and changed in PATCH request
        if 'irregular' in validated_data and validated_data['irregular'] is not instance.irregular:
            # Record the changes into the DB
            super().update(instance, validated_data)
            # Then check if irregular is False
            if (instance.irregular is False):
                # And if so, remove all current subjects
                instance.subjects.clear()
                # And add the ones matching the required criteria
                self.add_subjects(instance)

        # If year_level is updated and changed in PATCH request
        elif 'year_level' in validated_data and validated_data['year_level'] is not instance.year_level or instance.year_level is None:
            # Record the changes into the DB
            super().update(instance, validated_data)
            # If so, remove all current subjects
            instance.subjects.clear()
            # And add the ones matching the required criteria
            self.add_subjects(instance)

        # If semester is updated and changed in PATCH request
        elif 'semester' in validated_data and validated_data['semester'] is not instance.semester or instance.semester is None:
            # Record the changes into the DB
            super().update(instance, validated_data)
            # If so, remove all current subjects
            instance.subjects.clear()
            # And add the ones matching the required criteria
            self.add_subjects(instance)

        # If course is updated and changed in PATCH request
        elif 'course' in validated_data and validated_data['course'] is not instance.course or instance.course is None:
            # Record the changes into the DB
            super().update(instance, validated_data)
            # If so, remove all current subjects
            instance.subjects.clear()
            # And add the ones matching the required criteria
            self.add_subjects(instance)

        # Finally, update the instance with the validated data and return it
        return super().update(instance, validated_data)

    def add_subjects(self, instance):
        # Get the matching subjects based on the user's course, year level, and semester
        matching_subjects = SubjectInstance.objects.filter(
            course=instance.course, year_level=instance.year_level, semester=instance.semester)
        # Add the matching subjects to the user's subjects list
        print(matching_subjects)
        instance.subjects.add(*matching_subjects)


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

        StudentStatus.objects.update_or_create(
            user=user,
            defaults={
                'active': False,
                'location': Point(0, 0),
                'subject': None
            }
        )
        return user
