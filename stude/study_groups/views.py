from django.shortcuts import render
from rest_framework import generics
from .serializers import StudyGroupSerializer
from .models import StudyGroup
# Create your views here.


class StudyGroupListView(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()


class StudyGroupMembershipViewSet(generics.ListAPIView):
    serializer_class = StudyGroupSerializer
    queryset = StudyGroup.objects.all()
