from django.urls import include, path
from .views import StudyGroupListView, StudyGroupListNearView, StudyGroupCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'create', StudyGroupCreateView,
                basename='Create Study Group')

urlpatterns = [
    path('', StudyGroupListView.as_view()),
    path('near/', StudyGroupListNearView.as_view()),
    path('', include(router.urls)),
]
