from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StudentStatus
from .serializers import StudentStatusSerializer


class StudentStatusAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return StudentStatus.objects.get(user=user)


class ActiveStudentStatusListAPIView(generics.ListAPIView):
    serializer_class = StudentStatusSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StudentStatus.objects.filter(active=True)
