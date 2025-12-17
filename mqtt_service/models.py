"""
Models for MQTT Service
"""
from django.db import models


class MQTTMessage(models.Model):
    """Model to store MQTT messages"""
    topic = models.CharField(max_length=255)
    payload = models.TextField()
    qos = models.IntegerField(default=0)
    retain = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['topic', '-timestamp']),
            models.Index(fields=['processed', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.topic} - {self.timestamp}"


class MQTTConnection(models.Model):
    """Model to track MQTT connection status"""
    STATUS_CHOICES = [
        ('connected', 'Connected'),
        ('disconnected', 'Disconnected'),
        ('error', 'Error'),
    ]

    client_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='disconnected')
    last_connected = models.DateTimeField(null=True, blank=True)
    last_disconnected = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_id} - {self.status}"
