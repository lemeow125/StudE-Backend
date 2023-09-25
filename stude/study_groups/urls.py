from django.urls import include, path
from .views import StudyGroupListView, StudyGroupListNearView

urlpatterns = [
    path('', StudyGroupListView.as_view()),
    path('near/', StudyGroupListNearView.as_view()),
]
