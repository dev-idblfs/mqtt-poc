"""
URL Configuration for MQTT Service API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MQTTMessageViewSet, MQTTConnectionViewSet

router = DefaultRouter()
router.register(r'messages', MQTTMessageViewSet, basename='mqtt-message')
router.register(r'connections', MQTTConnectionViewSet,
                basename='mqtt-connection')

urlpatterns = [
    path('', include(router.urls)),
]
