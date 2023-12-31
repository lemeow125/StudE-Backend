from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentStatusAPIView, ActiveStudentStatusListAPIView, StudentStatusListByStudentStatusLocation, StudentStatusListByCurrentLocation

router = DefaultRouter()
router.register(r'near_current_location/', StudentStatusListByCurrentLocation,
                basename='Student Status based on current location')

urlpatterns = [
    path('self/', StudentStatusAPIView.as_view()),
    path('list/', ActiveStudentStatusListAPIView.as_view()),
    path('near/',
         StudentStatusListByStudentStatusLocation.as_view()),
    path('', include(router.urls)),
]
