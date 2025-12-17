"""
API Views for MQTT Service
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MQTTMessage, MQTTConnection
from .serializers import MQTTMessageSerializer, MQTTConnectionSerializer


class MQTTMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MQTT Messages
    - List all messages
    - Filter by topic and processed status
    - Mark messages as processed
    """
    queryset = MQTTMessage.objects.all()
    serializer_class = MQTTMessageSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic', 'processed']
    search_fields = ['topic', 'payload']
    ordering_fields = ['timestamp', 'topic']
    ordering = ['-timestamp']

    @action(detail=False, methods=['post'])
    def mark_processed(self, request):
        """Mark multiple messages as processed"""
        topic = request.data.get('topic')
        if not topic:
            return Response(
                {'error': 'topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_count = MQTTMessage.objects.filter(
            topic=topic,
            processed=False
        ).update(processed=True)

        return Response({
            'status': 'success',
            'updated_count': updated_count,
            'message': f'{updated_count} messages marked as processed'
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get message statistics"""
        total_messages = MQTTMessage.objects.count()
        unprocessed_messages = MQTTMessage.objects.filter(
            processed=False).count()
        topics = MQTTMessage.objects.values('topic').distinct().count()

        return Response({
            'total_messages': total_messages,
            'unprocessed_messages': unprocessed_messages,
            'unique_topics': topics,
        })


class MQTTConnectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MQTT Connection Status
    - View connection status
    - Check last connected time
    """
    queryset = MQTTConnection.objects.all()
    serializer_class = MQTTConnectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['client_id']

    @action(detail=False, methods=['get'])
    def current_status(self, request):
        """Get current connection status"""
        try:
            connection = MQTTConnection.objects.latest('updated_at')
            serializer = self.get_serializer(connection)
            return Response(serializer.data)
        except MQTTConnection.DoesNotExist:
            return Response(
                {'error': 'No connection status found'},
                status=status.HTTP_404_NOT_FOUND
            )
