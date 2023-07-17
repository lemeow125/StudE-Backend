from django.urls import include, path
from .views import SubjectListView
from .views import SubjectByYearSemesterView

urlpatterns = [
    path('', SubjectListView.as_view()),
    path('<slug:course_slug>/<slug:year_slug>/<slug:semester_slug>',
         SubjectByYearSemesterView.as_view()),
]
