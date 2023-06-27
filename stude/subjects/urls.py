from django.urls import include, path
from .views import SubjectListView
from .views import SubjectByYearSemesterView

urlpatterns = [
    path('', SubjectListView.as_view()),
    path('subjects/<str:year_slug>/',
         SubjectByYearSemesterView.as_view()),
]
