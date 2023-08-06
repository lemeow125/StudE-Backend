from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentStatusAPIView, ActiveStudentStatusListAPIView

urlpatterns = [
    path('self/', StudentStatusAPIView.as_view()),
    path('list/', ActiveStudentStatusListAPIView.as_view()),
]
