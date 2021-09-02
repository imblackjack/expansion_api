from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from apps.projects import views

router = DefaultRouter()
router.register(r'^projects', views.ProjectViewSet)

urlpatterns = [
    url(r'^code_trans', views.TransCode.as_view()),
    url(r'^command_run', views.RunCommand.as_view()),
    url(r'', include(router.urls))
]