from django.urls import include, path
from .views import CourseListView

urlpatterns = [
    path('', CourseListView.as_view()),
]
