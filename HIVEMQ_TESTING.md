# HiveMQ MQTT Testing Guide

## ✅ Status

Your Django MQTT POC is now **LIVE and CONNECTED** to HiveMQ Cloud at port 8883 with TLS/SSL.

- **Server Running**: http://127.0.0.1:8001/
- **API Endpoint**: http://127.0.0.1:8001/api/messages/
- **Admin Panel**: http://127.0.0.1:8001/admin/
- **MQTT Broker**: 3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud:8883
- **Subscribed Topics**: `mqtt/poc/`, `mqtt/data/`
- **Connection Status**: ✅ Connected

---

## Publishing Messages to HiveMQ

You have two options to publish messages:

### Option 1: HiveMQ Web Client (Easiest)

1. **Open HiveMQ Web UI**

   - Go to: https://console.hivemq.cloud/
   - Log in with your HiveMQ account

2. **Navigate to Clients**

   - Click "Clients" in the left menu

3. **Use Web Client**

   - Look for "Web Client" or use the broker's test client
   - Connect with your credentials

4. **Publish a Test Message**
   ```
   Topic: mqtt/poc/sensor1
   Payload: {"temperature": 25.5, "humidity": 60, "device": "sensor-001"}
   QoS: 0
   Retain: unchecked
   ```

### Option 2: mosquitto_pub (Command Line)

First, install Mosquitto client tools:

```bash
# macOS
brew install mosquitto

# Linux (Ubuntu/Debian)
sudo apt-get install mosquitto-clients

# Windows
# Download from: https://mosquitto.org/download/
```

**Publish a message:**

```bash
mosquitto_pub \
  -h 3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud \
  -p 8883 \
  -u hivemq.webclient.1765957386975 \
  -P "15.tdXp?,wJb>A8EmF0P" \
  -t mqtt/poc/sensor1 \
  --cafile /etc/ssl/certs/ca-certificates.crt \
  -m '{"temperature": 25.5, "humidity": 60, "device": "sensor-001"}'
```

**On macOS** (if certificate issue):

```bash
mosquitto_pub \
  -h 3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud \
  -p 8883 \
  -u hivemq.webclient.1765957386975 \
  -P "15.tdXp?,wJb>A8EmF0P" \
  -t mqtt/poc/sensor1 \
  -m '{"temperature": 25.5, "humidity": 60, "device": "sensor-001"}'
```

### Option 3: Python MQTT Client

Create a test script `publish_test.py`:

```python
import paho.mqtt.client as mqtt
import json
import time

BROKER = "3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "hivemq.webclient.1765957386975"
PASSWORD = "15.tdXp?,wJb>A8EmF0P"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ")
        # Publish test messages
        for i in range(5):
            topic = f"mqtt/poc/sensor{i}"
            payload = json.dumps({
                "temperature": 20 + i,
                "humidity": 50 + i*5,
                "device": f"sensor-{i:03d}",
                "timestamp": time.time()
            })
            client.publish(topic, payload, qos=0)
            print(f"Published to {topic}: {payload}")
            time.sleep(1)

        client.disconnect()
    else:
        print(f"Connection failed with code {rc}")

client = mqtt.Client(client_id="test-publisher", clean_session=True)
client.tls_set()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# Keep the script running for 30 seconds
time.sleep(30)
client.loop_stop()
```

**Run it:**

```bash
python publish_test.py
```

---

## Checking Received Messages

### Via API (Browser)

1. **View all messages**

   ```
   http://127.0.0.1:8001/api/messages/
   ```

2. **Filter by topic**

   ```
   http://127.0.0.1:8001/api/messages/?topic=mqtt/poc/sensor1
   ```

3. **View unprocessed messages**

   ```
   http://127.0.0.1:8001/api/messages/?processed=false
   ```

4. **Get statistics**
   ```
   http://127.0.0.1:8001/api/messages/statistics/
   ```

### Via Django Admin

1. Go to: http://127.0.0.1:8001/admin/
2. Login with credentials (create one if needed):
   ```bash
   python manage.py create_test_admin
   # Username: admin
   # Password: admin123
   ```
3. Click "MQTT Messages" to view all received messages
4. Use filters to search by topic, date, or processed status

### Via Django Shell

```bash
python manage.py shell
```

Then in the shell:

```python
from mqtt_service.models import MQTTMessage

# Get all messages
MQTTMessage.objects.all().order_by('-timestamp')[:5]

# Get messages from specific topic
MQTTMessage.objects.filter(topic='mqtt/poc/sensor1')

# Get unprocessed messages
MQTTMessage.objects.filter(processed=False)

# Mark messages as processed
MQTTMessage.objects.filter(topic='mqtt/poc/sensor1').update(processed=True)

# Get message count
MQTTMessage.objects.count()
```

---

## API Examples

### GET - List all messages with pagination

```bash
curl http://127.0.0.1:8001/api/messages/
```

Response:

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "topic": "mqtt/poc/sensor1",
      "payload": "{\"temperature\": 25.5, \"humidity\": 60}",
      "qos": 0,
      "retain": false,
      "timestamp": "2025-12-17T07:55:00Z",
      "processed": false
    }
  ]
}
```

### POST - Mark messages as processed

```bash
curl -X POST http://127.0.0.1:8001/api/messages/mark_processed/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "mqtt/poc/sensor1"}'
```

Response:

```json
{
  "status": "success",
  "updated_count": 1,
  "message": "1 messages marked as processed"
}
```

### GET - Message statistics

```bash
curl http://127.0.0.1:8001/api/messages/statistics/
```

Response:

```json
{
  "total_messages": 15,
  "unprocessed_messages": 8,
  "unique_topics": 3
}
```

### GET - Connection status

```bash
curl http://127.0.0.1:8001/api/connections/current_status/
```

Response:

```json
{
  "id": 1,
  "client_id": "django-mqtt-client",
  "status": "connected",
  "last_connected": "2025-12-17T07:52:44Z",
  "last_disconnected": null,
  "error_message": null,
  "created_at": "2025-12-17T07:48:00Z",
  "updated_at": "2025-12-17T07:52:44Z"
}
```

---

## Testing Workflow

### 1. Verify Connection

```bash
curl http://127.0.0.1:8001/api/connections/current_status/
# Should show "status": "connected"
```

### 2. Publish Test Message

Use any method above (Web UI, mosquitto_pub, or Python script)

### 3. Check API for Message

```bash
curl http://127.0.0.1:8001/api/messages/
# Should see your published message
```

### 4. View in Admin

1. Go to http://127.0.0.1:8001/admin/
2. Click "MQTT Messages"
3. Your message should appear

### 5. Mark as Processed

```bash
curl -X POST http://127.0.0.1:8001/api/messages/mark_processed/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "mqtt/poc/sensor1"}'
```

### 6. Verify Processing

```bash
curl http://127.0.0.1:8001/api/messages/?processed=false
# Message should no longer appear
```

---

## Subscription Topics

Your Django client is subscribed to:

- `mqtt/poc/` - Any message published to this topic or subtopics
- `mqtt/data/` - Any message published to this topic or subtopics

**Example topics that will be captured:**

- ✅ `mqtt/poc/sensor1`
- ✅ `mqtt/poc/device/temp`
- ✅ `mqtt/data/metrics`
- ✅ `mqtt/data/alerts`
- ❌ `other/topic` - Not subscribed

To add more topics, edit `.env`:

```
MQTT_TOPICS=mqtt/poc/,mqtt/data/,my/custom/topic/
```

Then restart the server.

---

## Troubleshooting

### No Messages Received

**Check 1: Verify Connection**

```bash
curl http://127.0.0.1:8001/api/connections/current_status/
```

Should show `"status": "connected"`

**Check 2: Check Logs**

```bash
tail -f logs/mqtt.log
```

**Check 3: Verify Topic**

- Message topic must match subscribed topics
- Check `.env` for `MQTT_TOPICS`

**Check 4: Test Publishing**

- Try publishing to `mqtt/poc/test` from HiveMQ Web Client
- Check API immediately: `http://127.0.0.1:8001/api/messages/`

### Connection Keeps Dropping

In development mode, Django's auto-reloader creates multiple instances. This causes code 7 errors (Protocol Error - client already connected). This is **normal** and one instance will stay connected.

To avoid this in production, disable auto-reloader:

```bash
python manage.py runserver --noreload
```

### Database Errors

Reset database:

```bash
rm db.sqlite3
python manage.py migrate
python manage.py create_test_admin
```

---

## Performance Tips

1. **Mark messages as processed** periodically to keep database clean
2. **Use filters** in API queries for large datasets
3. **Check statistics** to monitor message volume
4. **Configure pagination** in `settings.py` if needed

---

## Next Steps

1. ✅ **Connection Working** - MQTT client is connected
2. ✅ **API Available** - Test endpoints are working
3. 📝 **Publish Messages** - Send test data to HiveMQ
4. 📊 **Monitor Ingestion** - Check API for received messages
5. 🔌 **Integrate Apps** - Connect other services to the API
6. 🚀 **Deploy** - Move to production with proper configuration

---

**Credentials Reference:**

- HiveMQ Broker: `3296bfdeaf2d4e5ca161987c88d5a47c.s1.eu.hivemq.cloud:8883`
- MQTT Username: `hivemq.webclient.1765957386975`
- MQTT Password: `15.tdXp?,wJb>A8EmF0P`
- Django Admin: Create with `python manage.py create_test_admin`
- Django URL: `http://127.0.0.1:8001/`
