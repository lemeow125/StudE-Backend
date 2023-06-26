from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from accounts.models import CustomUser
from student_status.serializers import StudentStatusSerializer


class CustomUserSerializer(BaseUserSerializer):
    user_status = StudentStatusSerializer(
        source='studentstatus', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password',
                  'student_id_number', 'year_level', 'semester', 'avatar', 'is_banned', 'user_status')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username', 'email', 'password',
                  'student_id_number', 'year_level', 'semester', 'avatar')
