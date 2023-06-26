from rest_framework import serializers
from student_status.models import StudentStatus


class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = ('x_latitude', 'y_latitude', 'subject',
                  'year_level', 'semester', 'timestamp')
