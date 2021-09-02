from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.tasks import views

router = DefaultRouter()
router.register(r'^tasks', views.TaskViewSet)

urlpatterns = [
    url(r'^run_play', views.RunPlay.as_view()),
    url(r'', include(router.urls))
]