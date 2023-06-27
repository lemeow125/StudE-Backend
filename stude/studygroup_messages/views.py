from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from student_status.models import StudentStatus
from study_groups.models import StudyGroupMembership
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Message.objects.get(user=user)

    def get_queryset(self):
        user = self.request.user

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view messages of your current study group"
            )

        # Get student_status id of the current user
        student_status = StudentStatus.objects.filter(
            user=user.id
        ).values_list('study_group', flat=True).first()

        print("User ID:", user.id)
        print("Student_Status ID:", student_status)

        # Get the study group id
        print(StudyGroupMembership.objects.all())
        study_group_id_list = StudyGroupMembership.objects.filter(
            user=user.id).values_list('study_group').first()

        print("Study Group List:", study_group_id_list)

        # Now fetch the Messages matching the study group id
        messages = Message.objects.filter(study_group=study_group_id_list)
        return messages

    # To-do: only allow destroy of messages if message is by the same user
