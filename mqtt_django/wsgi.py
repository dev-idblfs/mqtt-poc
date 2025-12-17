"""
WSGI config for mqtt_django project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mqtt_django.settings')

application = get_wsgi_application()
