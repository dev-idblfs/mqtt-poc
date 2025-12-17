"""
MQTT Client Manager for handling MQTT connections and message reception
"""
import os
import logging
import time
import paho.mqtt.client as mqtt
from django.conf import settings
from django.utils import timezone
from .models import MQTTMessage, MQTTConnection

logger = logging.getLogger('mqtt_service')
client_id = f"{settings.MQTT_CLIENT_ID}-{os.getpid()}"


class MQTTClientManager:
    """Singleton class to manage MQTT client connection and message handling"""

    _instance = None
    _client = None
    _is_connected = False
    _connecting = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQTTClientManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls):
        """Initialize MQTT Client"""
        try:
            instance = cls()
            # Disconnect any existing client first
            if instance._client:
                try:
                    instance._client.loop_stop()
                    instance._client.disconnect()
                    time.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Error stopping old client: {e}")
            instance.connect()
        except Exception as e:
            logger.error(f"Failed to initialize MQTT client: {e}")

    def connect(self):
        """Establish MQTT connection"""
        if self._connecting:
            logger.debug("Already connecting, skipping...")
            return

        try:
            self._connecting = True

            # Stop any existing loop
            if self._client:
                try:
                    self._client.loop_stop()
                    self._client.disconnect()
                    time.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Error stopping existing client: {e}")

            logger.info("Initializing MQTT client...")

            self._client = mqtt.Client(
                client_id=client_id,
                clean_session=True
            )

            # Set callbacks
            self._client.on_connect = self._on_connect
            self._client.on_disconnect = self._on_disconnect
            self._client.on_message = self._on_message
            self._client.on_publish = self._on_publish
            self._client.on_subscribe = self._on_subscribe
            self._client.on_log = self._on_log

            # Set username and password if provided
            if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
                self._client.username_pw_set(
                    settings.MQTT_USERNAME,
                    settings.MQTT_PASSWORD
                )

            # Enable TLS for port 8883 (HiveMQ Cloud)
            if settings.MQTT_BROKER_PORT == 8883:
                self._client.tls_set()
                self._client.tls_insecure_set(False)
                logger.info("TLS enabled for MQTT connection")

            # Set automatic reconnect
            self._client.reconnect_delay_set(min_delay=1, max_delay=32)

            # Connect to broker
            logger.info(
                f"Connecting to MQTT broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}...")
            self._client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                keepalive=settings.MQTT_KEEPALIVE
            )

            # Subscribe to topics
            for topic in settings.MQTT_TOPICS:
                logger.info(f"Subscribing to topic: {topic}")
                self._client.subscribe(topic)

            # Start the network loop
            self._client.loop_start()
            logger.info("MQTT client started successfully")

        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
            self._update_connection_status('error', str(e))
        finally:
            self._connecting = False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        try:
            if self._client:
                self._client.loop_stop()
                self._client.disconnect()
                self._is_connected = False
                logger.info("MQTT client disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection"""
        if rc == 0:
            logger.info("MQTT client connected successfully")
            self._is_connected = True
            self._update_connection_status('connected')
        else:
            error_message = mqtt.connack_string(rc)
            logger.error(
                f"MQTT connection failed with code {rc}: {error_message}")
            self._update_connection_status('error', error_message)

    def _on_disconnect(self, client, userdata, rc):
        """Callback for MQTT disconnection"""
        if rc != 0:
            logger.warning(f"Unexpected MQTT disconnection with code {rc}")
            self._is_connected = False
            self._update_connection_status('disconnected')
        else:
            logger.info("MQTT client disconnected cleanly")
            self._is_connected = False
            self._update_connection_status('disconnected')

    def _on_message(self, client, userdata, msg):
        """Callback for receiving MQTT messages"""
        try:
            logger.debug(
                f"Message received on topic {msg.topic}: {msg.payload}")

            # Decode payload
            try:
                payload = msg.payload.decode('utf-8')
            except UnicodeDecodeError:
                payload = str(msg.payload)

            # Save message to database
            mqtt_message = MQTTMessage.objects.create(
                topic=msg.topic,
                payload=payload,
                qos=msg.qos,
                retain=msg.retain
            )

            logger.info(
                f"Message saved to database: {mqtt_message.id} from topic {msg.topic}")

        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    def _on_publish(self, client, userdata, mid):
        """Callback for message published"""
        logger.debug(f"Message published with id {mid}")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback for subscription"""
        logger.info(f"Subscription successful with QoS: {granted_qos}")

    def _on_log(self, client, userdata, level, buf):
        """Callback for logging"""
        if level == mqtt.MQTT_LOG_DEBUG:
            logger.debug(buf)
        elif level == mqtt.MQTT_LOG_INFO:
            logger.info(buf)
        elif level == mqtt.MQTT_LOG_NOTICE:
            logger.info(buf)
        elif level == mqtt.MQTT_LOG_WARNING:
            logger.warning(buf)
        elif level == mqtt.MQTT_LOG_ERR:
            logger.error(buf)

    def _update_connection_status(self, status, error_message=None):
        """Update connection status in database"""
        try:
            from django.db import connection as db_connection

            # Check if table exists
            with db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='mqtt_service_mqttconnection'
                """)
                if not cursor.fetchone():
                    logger.debug(
                        "mqtt_service_mqttconnection table not yet created")
                    return

            mqtt_conn, created = MQTTConnection.objects.get_or_create(
                client_id=client_id,
                defaults={'status': status}
            )

            mqtt_conn.status = status
            mqtt_conn.error_message = error_message

            if status == 'connected':
                mqtt_conn.last_connected = timezone.now()
            elif status == 'disconnected':
                mqtt_conn.last_disconnected = timezone.now()

            mqtt_conn.save()
            logger.info(f"Connection status updated: {status}")

        except Exception as e:
            logger.debug(
                f"Could not update connection status (table may not exist yet): {e}")

    @classmethod
    def get_instance(cls):
        """Get MQTT client manager instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def publish_message(cls, topic, payload, qos=0, retain=False):
        """Publish a message to MQTT broker"""
        manager = cls.get_instance()
        if manager._client and manager._is_connected:
            try:
                manager._client.publish(topic, payload, qos, retain)
                logger.info(f"Message published to topic {topic}")
                return True
            except Exception as e:
                logger.error(f"Error publishing message: {e}")
                return False
        else:
            logger.warning("MQTT client not connected, cannot publish message")
            return False
