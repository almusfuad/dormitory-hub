from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dormitory'

router = DefaultRouter()
router.register('list', views.DormitoryViewSet, basename='dormitory')

urlpatterns = [
      path('',include(router.urls)),
]