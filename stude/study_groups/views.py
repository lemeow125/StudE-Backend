from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer, StudyGroupCreateSerializer, StudyGroupDistanceSerializer
from .models import StudyGroup
from subjects.models import Subject, SubjectInstance
from student_status.models import StudentStatus
from rest_framework import generics, viewsets, exceptions
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

# Create your views here.


class StudyGroupCreateView(viewsets.ModelViewSet):
    http_method_names = ['patch', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupCreateSerializer
    queryset = StudyGroup.objects.all()


class StudyGroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):
        user = self.request.user

        # Get the user's course
        user_course = user.course
        print(user_course)

        # Get the subject name of the student's subjects from SubjectInstance
        user_subject_names = user.subjects.values_list('subject', flat=True)
        print('user subjects:', user_subject_names)
        # Get the corresponding Subject models
        user_subjects = Subject.objects.filter(name__in=user_subject_names)
        # Now fetch the StudyGroups with the matching Subject models
        studygroups = StudyGroup.objects.filter(subject__in=user_subjects)

        for group in studygroups:
            # Get all StudentStatus locations of the group
            group_locations = group.students.values_list('location', flat=True)
            # Convert string locations to GEOSGeometry objects
            point_locations = [fromstr(loc, srid=4326)
                               for loc in group_locations]

            # Calculate distances between every pair of locations
            distances = [(loc1.distance(
                loc2)*100000)for loc1 in point_locations for loc2 in point_locations]
            # Get the maximum distance
            group_radius = max(distances) if distances else 0
            group_radius = max(group_radius, 15)
            # Annotate the group with the radius
            group.radius = group_radius
        return studygroups


class StudyGroupListNearView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupDistanceSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):

        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()

        if user_status.active is False:
            raise exceptions.ValidationError("Student Status is not active")

        user_location = fromstr(
            user_status.location, srid=4326)

        # Get the user's course
        user_course = user.course
        print(user_course)

        # Get the subject name of the student's subjects from SubjectInstance
        user_subject_names = user.subjects.values_list('subject', flat=True)
        # Get the corresponding Subject models
        user_subjects = Subject.objects.filter(name__in=user_subject_names)

        # Now fetch the StudyGroups with the matching Subject models that are within 100m
        studygroups = StudyGroup.objects.filter(subject__in=user_subjects).annotate(
            distance=Distance('location', user_location)).filter(distance__lte=100)

        for group in studygroups:
            # Get all StudentStatus locations of the group
            group_locations = group.students.values_list('location', flat=True)
            # Convert string locations to GEOSGeometry objects
            point_locations = [fromstr(loc, srid=4326)
                               for loc in group_locations]
            # Calculate distances between every pair of locations
            distances = [(loc1.distance(
                loc2)*100000)for loc1 in point_locations for loc2 in point_locations]
            # Get the maximum distance
            group_radius = max(distances) if distances else 0
            group_radius = max(group_radius, 15)
            # Annotate the group with the radius
            group.radius = group_radius

        return studygroups


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user's student status matches the user field
        return obj.user == request.user.studentstatus
