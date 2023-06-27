from django.urls import include, path
from .views import StudyGroupListView, StudyGroupMembershipViewSet

urlpatterns = [
    path('', StudyGroupListView.as_view()),
    path('membership/', StudyGroupMembershipViewSet.as_view()),
]
