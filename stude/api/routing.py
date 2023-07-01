from django.urls import re_path
from channels.routing import URLRouter
import student_status.routing
import student_status.consumers
websocket_urlpatterns = [
    re_path(r'student_status/',
            URLRouter(student_status.routing.websocket_urlpatterns))
]
