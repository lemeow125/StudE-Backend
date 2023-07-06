from django.urls import path
from .views import StudentStatusAPIView, ActiveStudentStatusListAPIView

urlpatterns = [
    path('self/', StudentStatusAPIView.as_view()),
    path('list/', ActiveStudentStatusListAPIView.as_view()),
]
