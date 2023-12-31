from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('student_status/', include('student_status.urls')),
    path('courses/', include('courses.urls')),
    path('year_levels/', include('year_levels.urls')),
    path('semesters/', include('semesters.urls')),
    path('subjects/', include('subjects.urls')),
    path('study_groups/', include('study_groups.urls')),
    path('messages/', include('studygroup_messages.urls')),
    path('landmarks/', include('landmarks.urls')),
]
