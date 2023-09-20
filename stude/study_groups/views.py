from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer
from .models import StudyGroup
from subjects.models import Subject
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

        # Get the user's course
        user_course = user.course
        print(user_course)

        # Get subject names related to the user's course
        subject_names = Subject.objects.filter(
            course=user_course
        ).values_list('subject', flat=True)

        print(subject_names)

        # Now fetch the StudyGroups with the matching subject names
        studygroups = StudyGroup.objects.filter(subject_name__in=subject_names)
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

        # Get subject names related to the user's course
        subject_names = Subject.objects.filter(
            course=user_course
        ).values_list('subject', flat=True)

        print(subject_names)

        # Now fetch the StudyGroups with the matching subject names that are within 50m
        studygroups = StudyGroup.objects.filter(subject_name__in=subject_names).annotate(
            distance=Distance('location', user_location)).filter(distance__lte=50)
        return studygroups


class StudyGroupMembershipViewSet(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()
