from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer
from .models import StudyGroup
from subjects.models import Subject, SubjectInstance
from student_status.models import StudentStatus
from rest_framework import generics, viewsets, exceptions
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance

# Create your views here.


class StudyGroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):
        user = self.request.user

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

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

        return studygroups


class StudyGroupListNearView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_status = StudentStatus.objects.filter(user=user).first()
        user_location = fromstr(
            user_status.location, srid=4326)

        if user_status.active is False:
            raise exceptions.ValidationError("Student Status is not active")

        if not user.is_student:
            raise PermissionDenied(
                "You must be a student to view study groups"
            )

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
            group_locations = group.users.values_list('location', flat=True)
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


class StudyGroupMembershipViewSet(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()
