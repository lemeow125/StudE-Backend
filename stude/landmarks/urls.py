from django.urls import path
from .views import LandmarkListView

urlpatterns = [
    path('', LandmarkListView.as_view()),
]
