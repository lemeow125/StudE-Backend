from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from accounts.models import CustomUser
from student_status.serializers import StudentStatusSerializer
from student_status.models import StudentStatus


class CustomUserSerializer(BaseUserSerializer):
    user_status = StudentStatusSerializer(
        source='studentstatus', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password',
                  'student_id_number', 'year_level', 'semester', 'course', 'avatar', 'first_name', 'last_name', 'is_banned', 'user_status')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'email', 'password',
                  'student_id_number', 'year_level', 'semester', 'course', 'avatar', 'first_name', 'last_name')

    def create(self, validated_data):
        # Get the user's year_level and semester from the user model instance
        user = self.Meta.model(**validated_data)

        # Create a new user using the base serializer's create() method
        user = super().create(validated_data)

        # Create a student_status object for the user
        StudentStatus.objects.create(
            user=user,
            active=False,
            x=None,
            y=None,
            subject=None
        )

        return user
