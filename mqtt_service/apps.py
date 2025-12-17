"""
Apps Configuration for MQTT Service
"""
from django.apps import AppConfig


class MqttServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt_service'
    verbose_name = 'MQTT Service'

    def ready(self):
        """Initialize MQTT client when app is ready"""
        from .mqtt_client import MQTTClientManager
        import atexit

        # Initialize MQTT client
        MQTTClientManager.initialize()

        # Register cleanup on shutdown
        atexit.register(self._cleanup_mqtt)

    def _cleanup_mqtt(self):
        """Cleanup MQTT connection on app shutdown"""
        try:
            from .mqtt_client import MQTTClientManager
            manager = MQTTClientManager.get_instance()
            manager.disconnect()
        except:
            pass
