#!/usr/bin/env python
"""
HiveMQ Test Publisher Script
Publishes test MQTT messages to HiveMQ Cloud
"""
import paho.mqtt.client as mqtt
import json
import time
import sys

# HiveMQ Configuration
BROKER = "3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "hivemq.webclient.1765957386975"
PASSWORD = "15.tdXp?,wJb>A8EmF0P"
CLIENT_ID = "test-publisher-" + str(int(time.time()))

# Test data
TEST_MESSAGES = [
    {
        "topic": "mqtt/poc/sensor1",
        "data": {"temperature": 22.5, "humidity": 55, "device": "sensor-001", "location": "office"}
    },
    {
        "topic": "mqtt/poc/sensor2",
        "data": {"temperature": 18.3, "humidity": 45, "device": "sensor-002", "location": "warehouse"}
    },
    {
        "topic": "mqtt/poc/sensor3",
        "data": {"temperature": 25.1, "humidity": 65, "device": "sensor-003", "location": "lab"}
    },
    {
        "topic": "mqtt/data/metrics",
        "data": {"cpu": 45.2, "memory": 78.5, "disk": 62.1, "timestamp": int(time.time())}
    },
    {
        "topic": "mqtt/data/alerts",
        "data": {"alert_type": "temperature_high", "value": 28.5, "device": "sensor-001", "severity": "warning"}
    },
]

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker"""
    if rc == 0:
        print("✓ Connected to HiveMQ Cloud successfully!")
        return True
    else:
        print(f"✗ Connection failed with code {rc}")
        return False

def on_publish(client, userdata, mid):
    """Callback for when a message is published"""
    print(f"  Message published (id: {mid})")

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects"""
    if rc == 0:
        print("✓ Disconnected successfully")
    else:
        print(f"! Unexpected disconnection with code {rc}")

def publish_test_messages(count=1, delay=1):
    """Publish test messages to HiveMQ"""
    
    client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
    client.tls_set()
    client.username_pw_set(USERNAME, PASSWORD)
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    
    try:
        print("\n" + "="*60)
        print("HiveMQ MQTT Test Publisher")
        print("="*60)
        print(f"\nBroker: {BROKER}:{PORT}")
        print(f"Client ID: {CLIENT_ID}")
        print(f"Publishing {count} round(s) of messages...\n")
        
        client.connect(BROKER, PORT, keepalive=60)
        client.loop_start()
        
        # Wait for connection
        time.sleep(2)
        
        # Publish messages
        for round_num in range(count):
            if round_num > 0:
                print(f"\n--- Round {round_num + 1} ---")
            
            for message in TEST_MESSAGES:
                topic = message["topic"]
                payload = json.dumps(message["data"])
                
                print(f"Publishing to '{topic}':")
                print(f"  Payload: {payload}")
                
                client.publish(topic, payload, qos=0, retain=False)
                time.sleep(delay)
            
            if round_num < count - 1:
                print(f"\nWaiting {delay}s before next round...")
                time.sleep(delay)
        
        print("\n" + "="*60)
        print("✓ All messages published successfully!")
        print("="*60)
        print("\nNow check the API to verify messages were received:")
        print("  http://127.0.0.1:8001/api/messages/")
        print("\nOr view in Django admin:")
        print("  http://127.0.0.1:8001/admin/")
        print()
        
        time.sleep(1)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    # Get parameters from command line
    count = 1
    delay = 1
    
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Usage: python publish_test.py [rounds] [delay_seconds]")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            delay = int(sys.argv[2])
        except ValueError:
            print("Usage: python publish_test.py [rounds] [delay_seconds]")
            sys.exit(1)
    
    publish_test_messages(count, delay)
