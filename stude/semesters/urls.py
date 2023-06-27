from django.urls import include, path
from .views import SemesterListView

urlpatterns = [
    path('', SemesterListView.as_view()),
]
