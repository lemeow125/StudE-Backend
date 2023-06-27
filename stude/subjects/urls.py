from django.urls import include, path
from .views import SubjectListView
from .views import SubjectByYearSemesterView, SubjectByYearView

urlpatterns = [
    path('', SubjectListView.as_view()),
    path('<slug:year_slug>/',
         SubjectByYearView.as_view()),
    path('<slug:year_slug>/<slug:semester_slug>',
         SubjectByYearSemesterView.as_view()),
]
