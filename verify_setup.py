#!/usr/bin/env python
"""
Test script to verify Django MQTT POC setup
"""
from mqtt_service.models import MQTTMessage, MQTTConnection
from django.contrib.auth.models import User
from django.conf import settings
import os
import sys
import django

# Set Django settings BEFORE any imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mqtt_django.settings')

# Configure Django
django.setup()

# Now import Django components AFTER setup

print("✓ Django setup successful")

# Check models
print(f"✓ MQTTMessage model: {MQTTMessage._meta.db_table}")
print(f"✓ MQTTConnection model: {MQTTConnection._meta.db_table}")

# Check admin user
if User.objects.filter(username='admin').exists():
    print("✓ Admin user exists: admin")
else:
    print("⚠ No admin user found. Run: python manage.py create_test_admin")

# Check MQTT settings
print(f"\n✓ MQTT Configuration:")
print(f"  - Broker: {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}")
print(f"  - Client ID: {settings.MQTT_CLIENT_ID}")
print(f"  - Topics: {', '.join(settings.MQTT_TOPICS)}")

print("\n✓ Setup verification complete!")
print("\nNext steps:")
print("1. Update .env with your MQTT broker credentials")
print("2. Create admin user: python manage.py create_test_admin")
print("3. Start the server: python manage.py runserver")
print("4. Access API at: http://localhost:8000/api/")
print("5. Access admin at: http://localhost:8000/admin/")
