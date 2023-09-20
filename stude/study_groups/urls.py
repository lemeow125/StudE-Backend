from django.urls import include, path
from .views import StudyGroupListView, StudyGroupListNearView, StudyGroupMembershipViewSet

urlpatterns = [
    path('', StudyGroupListView.as_view()),
    path('near/', StudyGroupListNearView.as_view()),
    path('membership/', StudyGroupMembershipViewSet.as_view()),
]
