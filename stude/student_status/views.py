from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StudentStatus
from .serializers import StudentStatusSerializer


class StudentStatusAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = StudentStatus.objects.filter(user=user)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


class ActiveStudentStatusListAPIView(generics.ListAPIView):
    serializer_class = StudentStatusSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StudentStatus.objects.filter(active=True and user != user)
