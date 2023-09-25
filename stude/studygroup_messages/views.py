from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from student_status.models import StudentStatus
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()
        user_study_group = user_status.study_group
        serializer.save(user=user, study_group=user_study_group)

    def get_queryset(self):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()
        user_study_group = user_status.study_group

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view messages of your current study group"
            )

        if not user_study_group:
            raise PermissionDenied(
                "You are currently do not have a study group"
            )

        # Get student_status id of the current user
        student_status = StudentStatus.objects.filter(
            user=user.id
        ).values_list('study_group', flat=True).first()

        print("User ID:", user.id)
        print("Student_Status ID:", student_status)
        print("User Study Group:", user_study_group)

        # Now fetch the Messages matching the study group id
        messages = Message.objects.filter(
            study_group=user_study_group).order_by('-timestamp')
        return messages
