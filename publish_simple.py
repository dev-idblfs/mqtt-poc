#!/usr/bin/env python
"""
Simple HiveMQ Test - Send 5 test messages
Run in a separate terminal from the Django server
"""
import time
import json
import paho.mqtt.client as mqtt
import django
import os
import sys

# Add project to path
sys.path.insert(0, '/Users/divyanshu/projects/mqtt-poc')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mqtt_django.settings')

django.setup()


BROKER = "3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "hivemq.webclient.1765957386975"
PASSWORD = "15.tdXp?,wJb>A8EmF0P"


def publish_messages():
    client = mqtt.Client(
        client_id=f"test-pub-{int(time.time())}", clean_session=True)
    client.tls_set()
    client.username_pw_set(USERNAME, PASSWORD)

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    time.sleep(1)

    messages = [
        ("mqtt/poc/sensor1", {"temp": 22.5, "humidity": 55}),
        ("mqtt/poc/sensor2", {"temp": 18.3, "humidity": 45}),
        ("mqtt/data/metrics", {"cpu": 45, "memory": 78}),
        ("mqtt/poc/alarm", {"alert": "HIGH_TEMP", "value": 28}),
        ("mqtt/data/status", {"status": "OK", "timestamp": int(time.time())}),
    ]

    for topic, data in messages:
        payload = json.dumps(data)
        print(f"📤 Publishing to '{topic}': {payload}")
        client.publish(topic, payload, qos=0)
        time.sleep(0.5)

    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    print("\n✓ Publish complete! Check the API:")
    print("  http://127.0.0.1:8001/api/messages/")


if __name__ == "__main__":
    publish_messages()
