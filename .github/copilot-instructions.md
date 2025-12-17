# Django MQTT POC - Project Instructions

## Project Overview
This is a Django-based MQTT Proof of Concept (POC) application that receives MQTT messages from an MQTT broker and stores them in a database with a REST API interface.

## Key Features
- MQTT client integration using paho-mqtt
- Automatic message reception and storage
- REST API for querying messages
- Connection status tracking
- Django admin interface
- Comprehensive logging

## Project Structure
- `mqtt_django/` - Django project settings and configuration
- `mqtt_service/` - Django app containing MQTT functionality
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables

## Setup Instructions
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy and configure: `cp .env.example .env` (add MQTT credentials)
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`

## MQTT Configuration Required
You need to provide:
- MQTT_BROKER_HOST - Your MQTT broker hostname
- MQTT_BROKER_PORT - MQTT broker port (default 1883)
- MQTT_USERNAME - MQTT authentication username
- MQTT_PASSWORD - MQTT authentication password
- MQTT_TOPICS - Topics to subscribe to (comma-separated)

## Development Notes
- Logging is configured in settings.py
- MQTT client connects automatically on app startup
- Messages are stored in MQTTMessage model
- Connection status tracked in MQTTConnection model
- REST API endpoints available at /api/

## Common Commands
```bash
python manage.py migrate          # Run database migrations
python manage.py createsuperuser  # Create admin user
python manage.py runserver        # Start development server
python manage.py shell            # Django shell for testing
```

## Testing
- Use mosquitto_pub to send test messages
- Check API at http://localhost:8000/api/messages/
- View admin at http://localhost:8000/admin/
