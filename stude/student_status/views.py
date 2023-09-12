from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import Point
from requests import Response
from rest_framework import generics, viewsets, exceptions
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from .models import StudentStatus
from .serializers import StudentStatusLocationSerializer, StudentStatusSerializer
from subjects.models import Subject, SubjectInstance


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
        return StudentStatus.objects.exclude(user=user).filter(active=True)


class StudentStatusListByStudentStatusLocation(generics.ListAPIView):
    serializer_class = StudentStatusLocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()

        user_location = fromstr(
            user_status.location, srid=4326)

        if user_status.active is False:
            raise exceptions.ValidationError("Student Status is not active")

        # Get names of all subjects of the user
        user_subject_names = user.subjects.values_list('subject', flat=True)

        # Exclude user
        # Filter those only with the same subjects as the user
        # Annotate the queryset with distance to the user
        # Then filter so that only those within 50m remain
        return StudentStatus.objects.exclude(user=user).filter(active=True).filter(
            subject__name__in=user_subject_names).annotate(distance=Distance('location', user_location)).filter(distance__lte=50)


class StudentStatusListByCurrentLocation(viewsets.ViewSet):
    serializer_class = StudentStatusLocationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request):
        user = self.request.user
        location_str = request.data.get('location')

        # If location is not specified in request, throw error
        if not location_str:
            raise exceptions.ValidationError("Location is required")

        # Parse user location from the POST request
        user_location = fromstr(location_str, srid=4326)

        # Get names of all subjects of the user
        user_subject_names = user.subjects.values_list('subject', flat=True)

        # Exclude user
        # Filter those only with the same subjects as the user
        # Annotate the queryset with distance to the user
        # Then filter so that only those within 50m remain
        queryset = StudentStatus.objects.exclude(user=user).filter(active=True).filter(subject__name__in=user_subject_names).annotate(
            distance=Distance('location', user_location)).filter(distance__lte=50)
        serializer = StudentStatusLocationSerializer(queryset, many=True)
        return Response(serializer.data)
