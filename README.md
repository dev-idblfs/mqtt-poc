# Django MQTT POC

A Proof of Concept (POC) Django application that receives MQTT messages from an MQTT broker and stores them in a database. This POC demonstrates how to integrate paho-mqtt with Django to handle real-time message ingestion.

## Features

- **MQTT Integration**: Automatically connects to an MQTT broker and subscribes to specified topics
- **Message Storage**: Stores received MQTT messages in Django ORM models
- **REST API**: Provides RESTful API endpoints to query stored messages and connection status
- **Connection Management**: Tracks MQTT connection status and errors
- **Logging**: Comprehensive logging for debugging and monitoring
- **Admin Interface**: Django admin interface to manage and view MQTT messages
- **Message Processing**: Mark messages as processed for workflow management

## Project Structure

```
mqtt-poc/
├── mqtt_django/          # Django project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── mqtt_service/         # Django app for MQTT functionality
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── mqtt_client.py   # MQTT client manager
│   ├── serializers.py   # DRF serializers
│   └── urls.py          # App URL configuration
├── manage.py            # Django management command
├── requirements.txt     # Python dependencies
└── .env.example         # Example environment variables
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MQTT credentials**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your MQTT broker credentials:

   ```
   MQTT_BROKER_HOST=your-mqtt-broker.com
   MQTT_BROKER_PORT=1883
   MQTT_USERNAME=your-username
   MQTT_PASSWORD=your-password
   MQTT_TOPICS=mqtt/poc/+,mqtt/data/+
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser for admin access**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### MQTT Messages

- **List all messages**

  ```
  GET /api/messages/
  ```

  Query parameters:

  - `topic` - Filter by topic
  - `processed` - Filter by processed status (true/false)
  - `search` - Search in topic and payload
  - `ordering` - Order by field (-timestamp, topic)

- **Get message details**

  ```
  GET /api/messages/{id}/
  ```

- **Mark messages as processed**

  ```
  POST /api/messages/mark_processed/
  Body: {"topic": "mqtt/poc/sensor1"}
  ```

- **Get statistics**
  ```
  GET /api/messages/statistics/
  ```

### MQTT Connections

- **List connection status**

  ```
  GET /api/connections/
  ```

- **Get current connection status**
  ```
  GET /api/connections/current_status/
  ```

## Usage Example

### Testing with MQTT Publish

1. **Publish a message to your MQTT broker**

   ```bash
   mosquitto_pub -h your-mqtt-broker.com -u your-username -P your-password -t mqtt/poc/sensor1 -m '{"temperature": 25.5, "humidity": 60}'
   ```

2. **Check the API for received messages**

   ```bash
   curl http://localhost:8000/api/messages/
   ```

3. **Filter by topic**

   ```bash
   curl http://localhost:8000/api/messages/?topic=mqtt/poc/sensor1
   ```

4. **View connection status**
   ```bash
   curl http://localhost:8000/api/connections/current_status/
   ```

## Admin Interface

Access Django admin at `http://localhost:8000/admin/`

- View all received MQTT messages
- Check connection status
- Filter and search messages by topic and timestamp
- Manage processed status of messages

## Logging

Logs are written to console and file (logs/mqtt.log) with DEBUG level for mqtt_service app.

Example log outputs:

```
DEBUG 2025-01-15 10:30:45 mqtt_client 12345 67890 Connecting to MQTT broker...
INFO 2025-01-15 10:30:46 mqtt_client 12345 67890 MQTT client connected successfully
INFO 2025-01-15 10:30:47 mqtt_client 12345 67890 Message received on topic mqtt/poc/sensor1
```

## Environment Variables

| Variable         | Default                                           | Description                                |
| ---------------- | ------------------------------------------------- | ------------------------------------------ |
| DEBUG            | True                                              | Django debug mode                          |
| SECRET_KEY       | django-insecure-mqtt-poc-key-change-in-production | Django secret key                          |
| ALLOWED_HOSTS    | localhost,127.0.0.1                               | Allowed hostnames                          |
| MQTT_BROKER_HOST | localhost                                         | MQTT broker hostname                       |
| MQTT_BROKER_PORT | 1883                                              | MQTT broker port                           |
| MQTT_USERNAME    |                                                   | MQTT username                              |
| MQTT_PASSWORD    |                                                   | MQTT password                              |
| MQTT_CLIENT_ID   | django-mqtt-client                                | MQTT client identifier                     |
| MQTT_TOPICS      | mqtt/poc/+                                        | MQTT topics to subscribe (comma-separated) |
| MQTT_KEEPALIVE   | 60                                                | MQTT keepalive interval in seconds         |

## Troubleshooting

### Connection Issues

1. **Check MQTT broker connectivity**

   ```bash
   mosquitto_sub -h your-mqtt-broker.com -u your-username -P your-password -t mqtt/poc/+ -v
   ```

2. **Verify credentials** in `.env` file

3. **Check Django logs** for connection errors
   ```bash
   tail -f logs/mqtt.log
   ```

### Database Issues

1. **Run migrations**

   ```bash
   python manage.py migrate
   ```

2. **Check database permissions**

## Production Deployment

### Important Security Notes

1. Change `SECRET_KEY` in settings
2. Set `DEBUG = False` in production
3. Use environment variables for sensitive data
4. Use a production database (PostgreSQL recommended)
5. Set up proper SSL/TLS for MQTT connections
6. Use MQTT_USERNAME and MQTT_PASSWORD
7. Configure firewall rules
8. Use reverse proxy (nginx/Apache)

### Database Setup (PostgreSQL)

```bash
pip install psycopg2-binary
```

Update settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mqtt_db',
        'USER': 'mqtt_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Run with Gunicorn

```bash
gunicorn mqtt_django.wsgi:application --bind 0.0.0.0:8000
```

## Next Steps

- Add data validation for MQTT payloads
- Implement message processing workers
- Add webhooks for real-time notifications
- Create dashboard for visualization
- Implement message retention policies
- Add authentication for API endpoints
- Set up CI/CD pipeline

## Support

For issues and questions, please check the logs and Django documentation.

## License

This is a POC project. Use as needed for your requirements.
# mqtt-poc
# mqtt-poc
# mqtt-poc
# mqtt-poc
