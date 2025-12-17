# Django MQTT POC - Setup Complete! 🎉

## Project Ready

Your Django MQTT Proof of Concept is now fully set up and running. The development server is running at **http://127.0.0.1:8000/**

## Quick Start

### 1. **Update MQTT Credentials** (IMPORTANT)

Edit `.env` file in the project root with your MQTT broker details:

```bash
MQTT_BROKER_HOST=your-mqtt-broker.example.com
MQTT_BROKER_PORT=1883
MQTT_USERNAME=your-username
MQTT_PASSWORD=your-password
MQTT_CLIENT_ID=django-mqtt-client
MQTT_TOPICS=mqtt/poc/+,mqtt/data/+
MQTT_KEEPALIVE=60
```

### 2. **Create Admin User**

```bash
python manage.py create_test_admin
# Credentials: admin / admin123
```

Or create your own:

```bash
python manage.py createsuperuser
```

### 3. **Access the Application**

- **Django Admin**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **Messages API**: http://localhost:8000/api/messages/
- **Connections API**: http://localhost:8000/api/connections/

## API Endpoints Reference

### List All MQTT Messages

```bash
curl http://localhost:8000/api/messages/
```

### Filter Messages by Topic

```bash
curl "http://localhost:8000/api/messages/?topic=mqtt/poc/sensor1"
```

### Filter Unprocessed Messages

```bash
curl "http://localhost:8000/api/messages/?processed=false"
```

### Mark Messages as Processed

```bash
curl -X POST http://localhost:8000/api/messages/mark_processed/ \
  -H "Content-Type: application/json" \
  -d '{"topic":"mqtt/poc/sensor1"}'
```

### Get Message Statistics

```bash
curl http://localhost:8000/api/messages/statistics/
```

### Check Connection Status

```bash
curl http://localhost:8000/api/connections/current_status/
```

## Testing with MQTT

### Publish Test Message

```bash
mosquitto_pub \
  -h your-mqtt-broker.com \
  -u your-username \
  -P your-password \
  -t mqtt/poc/sensor1 \
  -m '{"temperature": 25.5, "humidity": 60}'
```

### Subscribe to Topics (for testing)

```bash
mosquitto_sub \
  -h your-mqtt-broker.com \
  -u your-username \
  -P your-password \
  -t mqtt/poc/+ \
  -v
```

## Project Structure

```
mqtt-poc/
├── mqtt_django/                    # Django Project
│   ├── settings.py                 # Settings with MQTT config
│   ├── urls.py                     # URL routing
│   └── wsgi.py                     # WSGI config
├── mqtt_service/                   # Django App
│   ├── models.py                   # MQTTMessage, MQTTConnection models
│   ├── mqtt_client.py              # MQTT client implementation
│   ├── views.py                    # REST API views
│   ├── serializers.py              # DRF serializers
│   ├── admin.py                    # Django admin configuration
│   ├── urls.py                     # App URL routing
│   └── management/commands/        # Custom management commands
│       └── create_test_admin.py    # Create test admin user
├── manage.py                       # Django CLI
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                            # Your environment (DO NOT COMMIT)
├── db.sqlite3                      # SQLite database
├── logs/                           # Application logs
│   └── mqtt.log                    # MQTT service logs
└── README.md                       # Project documentation
```

## How It Works

1. **MQTT Client Connection**: The MQTT client automatically connects when Django starts (in `mqtt_service/apps.py`)

2. **Message Reception**: When MQTT messages arrive on subscribed topics, the `_on_message` callback saves them to the database

3. **Database Storage**: All messages are stored in the `MQTTMessage` model with:

   - Topic
   - Payload (message content)
   - QoS level
   - Retain flag
   - Timestamp
   - Processed status

4. **Connection Tracking**: Connection status is monitored in the `MQTTConnection` model

5. **REST API**: Django REST Framework provides full API access to messages and connection status

## Database Models

### MQTTMessage

- `id` - Primary key
- `topic` - MQTT topic
- `payload` - Message content
- `qos` - Quality of Service (0, 1, or 2)
- `retain` - Message retain flag
- `timestamp` - When received
- `processed` - Processing status

### MQTTConnection

- `id` - Primary key
- `client_id` - MQTT client identifier
- `status` - connected/disconnected/error
- `last_connected` - Last successful connection time
- `last_disconnected` - Last disconnection time
- `error_message` - Error details if connection failed
- `created_at` - Record creation time
- `updated_at` - Last update time

## Logging

Logs are written to both console and file:

- **File**: `logs/mqtt.log`
- **Level**: DEBUG (for mqtt_service)
- **Format**: `LEVEL TIMESTAMP MODULE PID THREAD MESSAGE`

Example:

```
INFO 2025-12-17 10:30:46 mqtt_client 12345 67890 MQTT client connected successfully
INFO 2025-12-17 10:30:47 mqtt_client 12345 67890 Message received on topic mqtt/poc/sensor1
```

## Common Tasks

### View Received Messages

```bash
# Django shell
python manage.py shell

# Then in shell:
>>> from mqtt_service.models import MQTTMessage
>>> MQTTMessage.objects.all().order_by('-timestamp')[:5]
```

### Check Connection Status

```bash
python manage.py shell
>>> from mqtt_service.models import MQTTConnection
>>> MQTTConnection.objects.latest('updated_at')
```

### Clear Old Messages

```bash
python manage.py shell
>>> from mqtt_service.models import MQTTMessage
>>> MQTTMessage.objects.filter(processed=True).delete()
```

## Troubleshooting

### MQTT Connection Refused

**Problem**: `Error connecting to MQTT broker: [Errno 61] Connection refused`

**Solutions**:

1. Verify MQTT broker is running
2. Check broker hostname in `.env`
3. Verify broker port (default 1883)
4. Check firewall rules

### No Messages Being Received

1. Verify MQTT_TOPICS in `.env`
2. Check Django logs: `tail -f logs/mqtt.log`
3. Test with mosquitto_sub to verify topic subscription
4. Verify MQTT credentials

### Database Errors

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py create_test_admin
```

### Port Already in Use

```bash
# Run on different port
python manage.py runserver 8001
```

## Next Steps

1. ✅ **Setup Complete** - MQTT client is running
2. 📝 **Configure MQTT** - Update `.env` with your broker credentials
3. 📊 **Test Messages** - Send MQTT messages and verify they're stored
4. 🔌 **Integration** - Integrate with your MQTT broker
5. 🚀 **Deployment** - Deploy to production with appropriate settings

## Production Deployment Checklist

- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up SSL/TLS for MQTT
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up proper environment variables
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up monitoring and alerting
- [ ] Enable API authentication
- [ ] Configure CORS if needed
- [ ] Set up database backups
- [ ] Use Gunicorn or uWSGI for production

## Support Files

- **README.md** - Full project documentation
- **.github/copilot-instructions.md** - Project guidelines
- **.env.example** - Environment variables template
- **verify_setup.py** - Setup verification script
- **manage.py** - Django management commands

---

**Project Status**: ✅ Ready for MQTT Integration  
**Last Updated**: December 17, 2025  
**Django Version**: 4.2.0  
**Python Version**: 3.13.5
