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
                  'student_id_number', 'year_level', 'semester', 'avatar', 'first_name', 'last_name', 'is_banned', 'user_status')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'email', 'password',
                  'student_id_number', 'year_level', 'semester', 'avatar', 'first_name', 'last_name')

    def create(self, validated_data):
        # Extract the necessary fields from validated_data
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        student_id_number = validated_data['student_id_number']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        # Get the user's year_level and semester from the user model instance
        user = self.Meta.model(**validated_data)
        year_level = user.year_level
        semester = user.semester

        # Create a new user using the base serializer's create() method
        user = super().create(validated_data)

        # Create a student_status object for the user
        student_status = StudentStatus.objects.create(
            user=user,
            year_level=year_level,
            semester=semester,
            active=False,
            x=None,
            y=None,
            subject=None
        )

        return user
