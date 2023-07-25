from django.urls import include, path
from .views import SubjectByCourseView, SubjectByCourseYearSemesterView, SubjectListView
from rest_framework import routers
urlpatterns = [
    path('', SubjectListView.as_view()),
    path('<slug:course_slug>',
         SubjectByCourseView.as_view()),
    path('<slug:course_slug>/<slug:year_slug>/<slug:semester_slug>',
         SubjectByCourseYearSemesterView.as_view()),
]
