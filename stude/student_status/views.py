from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import generics, viewsets, exceptions
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from .models import StudentStatus
from .serializers import StudentStatusLocationSerializer, StudentStatusSerializer


class StudentStatusAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        queryset = StudentStatus.objects.filter(user=user)
        obj = get_object_or_404(queryset)
        return obj


class ActiveStudentStatusListAPIView(generics.ListAPIView):
    serializer_class = StudentStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StudentStatus.objects.filter(active=True and user != user)


class StudentStatusListByStudentStatusLocation(generics.ListAPIView):
    serializer_class = StudentStatusLocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()
        print('User Location: ', user_status.location)
        if user_status.location is None:
            raise exceptions.ValidationError("User location is not set")
        user_location = fromstr(
            user_status.location, srid=4326)

        return StudentStatus.objects.filter(user != user).filter(subject__in=user.subjects.all()).annotate(distance=Distance('location', user_location)).filter(distance__lte=50)


class StudentStatusListByCurrentLocation(viewsets.ViewSet):
    serializer_class = StudentStatusLocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request):
        user = self.request.user
        location_str = request.data.get('location')
        if not location_str:
            raise exceptions.ValidationError("Location is required")

        user_location = fromstr(location_str, srid=4326)
        queryset = StudentStatus.objects.filter(user != user).filter(subject__in=user.subjects.all()).annotate(
            distance=Distance('location', user_location)).filter(distance__lte=50)
        serializer = StudentStatusLocationSerializer(queryset, many=True)
        return Response(serializer.data)
