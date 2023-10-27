from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .serializers import StudyGroupSerializer, StudyGroupCreateSerializer, StudyGroupDistanceSerializer, StudyGroupDetailSerializer, CustomUserAvatarSerializer
from .models import StudyGroup
from subjects.models import Subject, SubjectInstance
from student_status.models import StudentStatus
from rest_framework import generics, viewsets, exceptions
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from accounts.models import CustomUser

# Create your views here.


class StudyGroupAvatarsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserAvatarSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        # Get user
        user = self.request.user

        # Get status of user
        user_status = StudentStatus.objects.filter(user=user).first()

        # Return error if not in study group
        if (not user_status.study_group):
            raise exceptions.ValidationError("You are not in a study group")

        # Get study group of user
        user_study_group = user_status.study_group

        # Get students in that study group
        study_group_student_ids = user_study_group.students.values_list(
            'user', flat=True)

        # Then get user instances of those students
        study_group_users = CustomUser.objects.filter(
            id__in=study_group_student_ids)

        # Return to be parsed by serializer
        return study_group_users


class StudyGroupMembersAvatarView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupCreateSerializer
    queryset = CustomUser.objects.all()


class StudyGroupCreateView(viewsets.ModelViewSet):
    http_method_names = ['patch', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupCreateSerializer
    queryset = StudyGroup.objects.all()


class StudyGroupDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyGroupDetailSerializer
    queryset = StudyGroup.objects.all()
    lookup_field = 'name'


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
            # Get the number of students in a group
            student_count = group.students.values_list(
                'user', flat=True).count()
            # Each student will contribute 10 to the radius
            radius = student_count * 10

            # If the radius exceeds 50, set it back to 50
            if (radius > 50):
                radius = 50
            # (For debug purposes) If radius is less than 5, set it back to 5
            elif (radius < 5):
                radius = 5
            # Annotate the group with the radius
            group.radius = radius

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
