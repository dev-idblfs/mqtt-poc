"""
Django Admin Configuration for MQTT Service
"""
from django.contrib import admin
from .models import MQTTMessage, MQTTConnection


@admin.register(MQTTMessage)
class MQTTMessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'timestamp', 'processed', 'qos')
    list_filter = ('topic', 'processed', 'timestamp')
    search_fields = ('topic', 'payload')
    readonly_fields = ('timestamp',)


@admin.register(MQTTConnection)
class MQTTConnectionAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'status', 'last_connected', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('client_id',)
    readonly_fields = ('created_at', 'updated_at')
