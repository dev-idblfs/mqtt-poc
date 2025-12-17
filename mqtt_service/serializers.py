"""
Serializers for MQTT Service API
"""
from rest_framework import serializers
from .models import MQTTMessage, MQTTConnection


class MQTTMessageSerializer(serializers.ModelSerializer):
    """Serializer for MQTT Messages"""
    class Meta:
        model = MQTTMessage
        fields = ['id', 'topic', 'payload', 'qos',
                  'retain', 'timestamp', 'processed']
        read_only_fields = ['id', 'timestamp']


class MQTTConnectionSerializer(serializers.ModelSerializer):
    """Serializer for MQTT Connection Status"""
    class Meta:
        model = MQTTConnection
        fields = ['id', 'client_id', 'status', 'last_connected', 'last_disconnected',
                  'error_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
