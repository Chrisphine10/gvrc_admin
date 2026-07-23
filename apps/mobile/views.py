# -*- encoding: utf-8 -*-
"""
Mobile App API Views - Consolidated from all apps
"""

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Import models from different apps
from apps.chat.models import Conversation, Message
from apps.mobile.ai_service import generate_reply
from apps.mobile.directions_service import route as directions_route
from apps.facilities.models import Facility, FacilityContact, FacilityService, FacilityCoordinate
from apps.mobile_sessions.models import MobileSession
from apps.music.models import Music
from apps.documents.models import Document
from apps.lookups.models import (
    ServiceCategory, GBVCategory, ContactType, OwnerType,
    InfrastructureType, ConditionStatus, DocumentType
)
from apps.analytics.models import ContactInteraction

# Import serializers
from apps.chat.serializers import (
    ConversationSerializer, ConversationDetailSerializer, MessageSerializer,
    CreateConversationSerializer, CreateMessageSerializer, UpdateMessageStatusSerializer,
    MobileConversationListSerializer
)
from apps.api.serializers import (
    MobileAppFacilitySerializer, MobileAppFacilityListSerializer, MobileFacilityMapSerializer,
    MusicSerializer, DocumentSerializer,
    MobileSessionSerializer, MobileSessionCreateSerializer, MobileSessionUpdateSerializer, MobileSessionEndSerializer,
    FacilityContactSerializer
)

# Import services
from apps.chat.services import ConversationService, MessageService
from apps.mobile_sessions.services import MobileSessionService


class MobileSessionPermission(BasePermission):
    """
    Custom permission class for mobile API endpoints.
    Validates device_id and checks if mobile session exists and is active.
    Allows superadmin users to bypass mobile session requirement for chat actions.
    """
    
    message = "Valid mobile session required. Please provide a valid device_id."
    
    def has_permission(self, request, view):
        # Allow superadmin users to bypass mobile session requirement for chat actions
        if (request.user and request.user.is_authenticated and request.user.is_superuser and 
            hasattr(view, 'action') and view.action in ['list_conversations', 'get_conversation_detail', 'send_message', 'update_message_status', 'close_conversation']):
            return True
        
        # For GET requests, get device_id from query parameters
        # For POST/PUT requests, check both query parameters and request body
        if request.method == 'GET':
            device_id = request.query_params.get('device_id')
        else:
            # For POST requests, check query params first, then request body
            device_id = request.query_params.get('device_id') or request.data.get('device_id')
        
        if not device_id:
            self.message = "device_id is required. For GET requests, pass as query parameter. For POST requests, include in query parameters or request body."
            return False
        
        # Check if mobile session exists and is active
        try:
            session = MobileSession.objects.get(device_id=device_id, is_active=True)
            # Store session in request for use in views
            request.mobile_session = session
            return True
        except MobileSession.DoesNotExist:
            self.message = f"Mobile session not found or inactive for device_id: {device_id}. Please create a valid session first."
            return False


class MobileChatViewSet(viewsets.ViewSet):
    """
    Mobile Chat API endpoints
    
    Mobile users can:
    - Start/retrieve conversations (requires device_id in URL or query params)
    - Send messages via REST API (requires device_id in URL or query params)
    - Send messages via WebSocket for real-time chat (see websocket endpoint documentation)
    - Update message status (requires device_id in URL or query params)
    - View conversation history (requires device_id in URL or query params)
    
    WebSocket Endpoint:
    - Connect: ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx
    - For production: wss://host/ws/mobile/chat/{conversation_id}/?device_id=xxx
    - Supports real-time messaging, typing indicators, read receipts, and message status updates
    - See websocket endpoint for detailed documentation
    
    Superadmin users can:
    - Access all conversations without mobile session (device_id optional)
    - Send messages to any conversation (device_id optional)
    - Update any message status (device_id optional)
    - View any conversation detail (device_id optional)
    """
    
    permission_classes = []  # No authentication required - only device_id validation
    
    def _get_request_device_id(self, request):
        """Resolve device_id from query parameters or request body."""
        if request.method == 'GET':
            return request.query_params.get('device_id')
        return request.query_params.get('device_id') or request.data.get('device_id')
    
    def _validate_mobile_session(self, device_id):
        """
        Validate device_id and return mobile session if valid
        """
        if not device_id:
            return None, "device_id is required"
        
        try:
            session = MobileSession.objects.get(device_id=device_id, is_active=True)
            return session, None
        except MobileSession.DoesNotExist:
            return None, f"Mobile session not found or inactive for device_id: {device_id}"
    
    def _check_conversation_access(self, conversation, mobile_session):
        """
        Check if mobile session has access to the conversation
        """
        if not mobile_session:
            return False, "Mobile session required for mobile users"
        
        if conversation.mobile_session != mobile_session:
            return False, "Access denied to this conversation"
        
        return True, None
    
    def _get_conversation(self, pk):
        """Helper to fetch a conversation by public identifier."""
        return get_object_or_404(Conversation, conversation_id=pk)
    
    @swagger_auto_schema(
        operation_id="mobile_chat_start",
        operation_description="Start a new conversation or retrieve existing one. After getting the conversation_id, you can connect to the WebSocket endpoint for real-time chat: ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx",
        request_body=CreateConversationSerializer,
        responses={
            200: openapi.Response('Conversation data', ConversationSerializer),
            201: openapi.Response('Conversation created', ConversationSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=False, methods=['post'], url_path='start')
    def start_conversation(self, request):
        """Start a new conversation or retrieve existing one"""
        serializer = CreateConversationSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data.get('device_id')
            subject = serializer.validated_data.get('subject', '')
            
            # For superadmin users, device_id is optional
            if not device_id and (request.user and request.user.is_authenticated and request.user.is_superuser):
                # Superadmin users can access existing conversations but need device_id to create new ones
                return Response(
                    {'error': 'device_id is required even for superadmin users to create new conversations'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # For mobile users, device_id is required
            if not device_id:
                return Response(
                    {'error': 'device_id is required for mobile users'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                mobile_session = MobileSession.objects.get(device_id=device_id, is_active=True)
                
                # Check if there's already an open conversation for this device
                existing_conversation = Conversation.objects.filter(
                    mobile_session=mobile_session,
                    status__in=['new', 'active']  # Only consider new or active conversations as "open"
                ).order_by('-created_at').first()
                
                if existing_conversation:
                    # Return existing open conversation
                    response_serializer = ConversationSerializer(existing_conversation, context={'request': request})
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                
                # No open conversation exists, create a new one
                try:
                    conversation = ConversationService.get_or_create_conversation(mobile_session, subject)
                    
                    # If new conversation, auto-assign admin
                    if conversation.status == 'new':
                        ConversationService.auto_assign_conversation(conversation)
                    
                    response_serializer = ConversationSerializer(conversation, context={'request': request})
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(
                        {'error': f'Failed to create conversation: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                    
            except MobileSession.DoesNotExist:
                return Response(
                    {'error': 'Invalid or inactive device ID'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': f'Unexpected error: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id="mobile_chat_list",
        operation_description="List conversations for a mobile device or all conversations for superadmin users (device_id optional for superadmin)",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - required for mobile users, optional for superadmin", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Conversation list', MobileConversationListSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_conversations(self, request):
        """List conversations for a mobile device or all conversations for superadmin"""
        # If superadmin, return all conversations without requiring device_id
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            conversations = Conversation.objects.all().order_by('-last_message_at')
            serializer = MobileConversationListSerializer(conversations, many=True, context={'request': request})
            return Response(serializer.data)
        
        # For mobile users, require device_id
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response(
                {'error': 'device_id parameter is required for mobile users'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            mobile_session = MobileSession.objects.get(device_id=device_id, is_active=True)
            
            # Get conversations for this device, prioritizing open ones first
            conversations = Conversation.objects.filter(mobile_session=mobile_session).order_by(
                # Order by: last message time (newest first)
                '-last_message_at'
            )
            
            # Custom ordering to ensure open conversations appear first
            open_conversations = []
            closed_conversations = []
            
            for conv in conversations:
                if conv.status in ['new', 'active']:
                    open_conversations.append(conv)
                else:
                    closed_conversations.append(conv)
            
            # Sort open conversations by last message time (newest first), handle None values
            open_conversations.sort(
                key=lambda x: x.last_message_at if x.last_message_at is not None else x.created_at, 
                reverse=True
            )
            # Sort closed conversations by last message time (newest first), handle None values
            closed_conversations.sort(
                key=lambda x: x.last_message_at if x.last_message_at is not None else x.created_at, 
                reverse=True
            )
            
            # Combine: open conversations first, then closed ones
            ordered_conversations = open_conversations + closed_conversations
            
            serializer = MobileConversationListSerializer(ordered_conversations, many=True, context={'request': request})
            return Response(serializer.data)
            
        except MobileSession.DoesNotExist:
            return Response(
                {'error': 'Invalid or inactive device ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
    @swagger_auto_schema(
        operation_id="mobile_chat_get_conversation_detail",
        operation_description="Get conversation details with messages. Requires device_id in query params.",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - required for mobile users", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            200: openapi.Response('Conversation details', ConversationDetailSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=True, methods=['get'], url_path='detail')
    def get_conversation_detail(self, request, pk=None):
        """Get conversation details with messages"""
        conversation = self._get_conversation(pk)
        is_superadmin = request.user and request.user.is_authenticated and request.user.is_superuser
        
        if is_superadmin:
            serializer = ConversationDetailSerializer(conversation, context={'request': request})
            return Response(serializer.data)
        
        device_id = self._get_request_device_id(request)
        if not device_id:
            return Response(
                {'error': 'device_id is required in query parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session, error_message = self._validate_mobile_session(device_id)
        if not session:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        access_ok, error_msg = self._check_conversation_access(conversation, session)
        if not access_ok:
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ConversationDetailSerializer(conversation, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_id="mobile_chat_send_message",
        operation_description="Send a message in a conversation via REST API. Requires device_id for mobile users. For real-time messaging, use the WebSocket endpoint: ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - required for mobile users", type=openapi.TYPE_STRING, required=False
            )
        ],
        request_body=CreateMessageSerializer,
        responses={
            201: MessageSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
        tags=["Chat APIs"]
    )
    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """Send a message in a conversation"""
        conversation = self._get_conversation(pk)
        device_id = self._get_request_device_id(request)
        
        # For superadmin users, allow sending messages to any conversation
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            # Handle both form data (file uploads) and JSON data
            if request.content_type and 'multipart/form-data' in request.content_type:
                serializer = CreateMessageSerializer(data=request.data, files=request.FILES)
            else:
                serializer = CreateMessageSerializer(data=request.data)
                
            if serializer.is_valid():
                # Get validated data
                content = serializer.validated_data.get('content', '')
                message_type = serializer.validated_data.get('message_type', 'text')
                media_file = serializer.validated_data.get('media_file')
                media_url = serializer.validated_data.get('media_url', '')
                is_urgent = serializer.validated_data.get('is_urgent', False)
                metadata = serializer.validated_data.get('metadata', {})
                
                # Determine message type based on file if not specified or if it's still 'text'
                if media_file:
                    # Always determine message type from file content type, regardless of current message_type
                    if media_file.content_type.startswith('image/'):
                        message_type = 'image'
                    elif media_file.content_type.startswith('video/'):
                        message_type = 'file'  # We'll use 'file' for videos
                    elif media_file.content_type.startswith('audio/'):
                        message_type = 'voice'
                    else:
                        message_type = 'file'
                    
                    # If no content was provided, use a default caption
                    if not content:
                        content = f"Uploaded {message_type}"
                
                # Use admin message creation for superadmin users
                try:
                    message = MessageService.create_admin_message(
                        conversation=conversation,
                        content=content,
                        admin_user=request.user,
                        message_type=message_type,
                        media_file=media_file,
                        media_url=media_url,
                        is_urgent=is_urgent,
                        metadata=metadata
                    )
                    response_serializer = MessageSerializer(message, context={'request': request})
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(
                        {'error': f'Failed to create message: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not device_id:
            return Response(
                {'error': 'device_id is required for mobile users'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session, error_message = self._validate_mobile_session(device_id)
        if not session:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        access_ok, error_msg = self._check_conversation_access(conversation, session)
        if not access_ok:
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)
        
        # Handle both form data (file uploads) and JSON data
        if request.content_type and 'multipart/form-data' in request.content_type:
            serializer = CreateMessageSerializer(data=request.data, files=request.FILES)
        else:
            serializer = CreateMessageSerializer(data=request.data)
            
        if serializer.is_valid():
            # Get validated data
            content = serializer.validated_data.get('content', '')
            message_type = serializer.validated_data.get('message_type', 'text')
            media_file = serializer.validated_data.get('media_file')
            media_url = serializer.validated_data.get('media_url', '')
            is_urgent = serializer.validated_data.get('is_urgent', False)
            metadata = serializer.validated_data.get('metadata', {})
            
            # Determine message type based on file if not specified or if it's still 'text'
            if media_file:
                # Always determine message type from file content type, regardless of current message_type
                if media_file.content_type.startswith('image/'):
                    message_type = 'image'
                elif media_file.content_type.startswith('video/'):
                    message_type = 'file'  # We'll use 'file' for videos
                elif media_file.content_type.startswith('audio/'):
                    message_type = 'voice'
                else:
                    message_type = 'file'
                
                # If no content was provided, use a default caption
                if not content:
                    content = f"Uploaded {message_type}"
            
            try:
                message = MessageService.create_mobile_message(
                    conversation=conversation,
                    content=content,
                    message_type=message_type,
                    media_file=media_file,
                    media_url=media_url,
                    is_urgent=is_urgent,
                    metadata=metadata
                )
                response_serializer = MessageSerializer(message, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': f'Failed to create message: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id="mobile_chat_update_status",
        operation_description="Update message delivery status",
        request_body=UpdateMessageStatusSerializer,
        responses={
            200: openapi.Response('Message updated', MessageSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=False, methods=['put'], url_path='messages/(?P<message_id>[^/.]+)/status')
    def update_message_status(self, request, message_id=None):
        """Update message delivery status"""
        message = get_object_or_404(Message, message_id=message_id)
        
        # For superadmin users, allow updating any message status
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            serializer = UpdateMessageStatusSerializer(data=request.data)
            if serializer.is_valid():
                new_status = serializer.validated_data['status']
                
                if new_status == 'delivered':
                    MessageService.mark_message_delivered(message)
                elif new_status == 'read':
                    MessageService.mark_message_read(message)
                
                response_serializer = MessageSerializer(message, context={'request': request})
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # For mobile users, check if they have access to this message
        device_id = self._get_request_device_id(request)
        if not device_id:
            return Response(
                {'error': 'device_id is required for this endpoint'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session, error_message = self._validate_mobile_session(device_id)
        if session:
            access_ok, error_msg = self._check_conversation_access(message.conversation, session)
            if not access_ok:
                return Response(
                    {'error': error_msg}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'error': error_message}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UpdateMessageStatusSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            
            try:
                if new_status == 'delivered':
                    MessageService.mark_message_delivered(message)
                elif new_status == 'read':
                    MessageService.mark_message_read(message)
                else:
                    return Response(
                        {'error': f'Invalid status: {new_status}. Must be "delivered" or "read"'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                response_serializer = MessageSerializer(message, context={'request': request})
                return Response(response_serializer.data)
            except Exception as e:
                return Response(
                    {'error': f'Failed to update message status: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_id="mobile_chat_close_conversation",
        operation_description="Close a conversation for a mobile device",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - required for mobile users", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Conversation closed', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'conversation': openapi.Schema(type=openapi.TYPE_OBJECT)
            })),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=True, methods=['post'], url_path='close')
    def close_conversation(self, request, pk=None):
        """Close a conversation for a mobile device"""
        conversation = self._get_conversation(pk)
        device_id = self._get_request_device_id(request)
        
        # For superadmin users, allow closing any conversation
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            try:
                if conversation.status == 'closed':
                    response_serializer = ConversationSerializer(conversation, context={'request': request})
                    return Response({
                        'message': 'Conversation is already closed',
                        'conversation': response_serializer.data
                    }, status=status.HTTP_200_OK)
                
                conversation.status = 'closed'
                conversation.save()
                
                response_serializer = ConversationSerializer(conversation, context={'request': request})
                return Response({
                    'message': 'Conversation closed by admin',
                    'conversation': response_serializer.data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {'error': f'Failed to close conversation: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        if not device_id:
            return Response(
                {'error': 'device_id is required for mobile users'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session, error_message = self._validate_mobile_session(device_id)
        if not session:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        access_ok, error_msg = self._check_conversation_access(conversation, session)
        if not access_ok:
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if conversation is already closed
        if conversation.status == 'closed':
            response_serializer = ConversationSerializer(conversation, context={'request': request})
            return Response({
                'message': 'Conversation is already closed',
                'conversation': response_serializer.data
            }, status=status.HTTP_200_OK)
        
        # Close the conversation
        try:
            conversation.status = 'closed'
            conversation.save()
            
            response_serializer = ConversationSerializer(conversation, context={'request': request})
            return Response({
                'message': 'Conversation closed successfully',
                'conversation': response_serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to close conversation: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="mobile_chat_websocket_info",
        operation_description="Get WebSocket connection information for real-time chat. Connect to the WebSocket endpoint for bidirectional real-time messaging.",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - optional, used for documentation examples", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('WebSocket connection information', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'websocket_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='WebSocket connection URL template',
                        example='ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx'
                    ),
                    'websocket_url_production': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='WebSocket connection URL for production (WSS)',
                        example='wss://host/ws/mobile/chat/{conversation_id}/?device_id=xxx'
                    ),
                    'authentication': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Authentication method',
                        example='device_id query parameter'
                    ),
                    'features': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description='Supported features'
                    ),
                    'message_types': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Supported message types'
                    ),
                    'connection_flow': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_STRING),
                        description='Steps to connect'
                    ),
                    'documentation': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Full documentation file'
                    )
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=False, methods=['get'], url_path='websocket-info')
    def websocket_info(self, request):
        """Get WebSocket connection information for real-time chat"""
        from django.conf import settings
        
        # Get base URL from request or settings
        scheme = 'wss' if request.is_secure() or getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'ws'
        host = request.get_host()
        base_url = f"{scheme}://{host}"
        
        return Response({
            'websocket_url': f'{base_url}/ws/mobile/chat/{{conversation_id}}/?device_id={{device_id}}',
            'websocket_url_production': f'wss://{host}/ws/mobile/chat/{{conversation_id}}/?device_id={{device_id}}',
            'authentication': 'device_id query parameter (must correspond to active MobileSession)',
            'features': [
                'real-time bidirectional messaging',
                'typing indicators',
                'read receipts',
                'message status updates (sent, delivered, read)',
                'user presence notifications',
                'media support (images, files)',
                'urgent message flagging'
            ],
            'message_types': {
                'chat_message': 'Send and receive chat messages in real-time',
                'message_status': 'Update message delivery/read status',
                'typing_indicator': 'Show when user is typing',
                'read_receipt': 'Mark messages as read'
            },
            'connection_flow': [
                '1. Call POST /mobile/chat/start/ with device_id to get conversation_id',
                f'2. Connect to WebSocket: {base_url}/ws/mobile/chat/{{conversation_id}}/?device_id={{device_id}}',
                '3. Wait for connection_established message',
                '4. Start sending/receiving messages in real-time',
                '5. Use REST API endpoints for conversation management (list, close, etc.)'
            ],
            'example_connection': {
                'javascript': 'const ws = new WebSocket(`wss://host/ws/mobile/chat/123/?device_id=abc123`);',
                'python': 'import websockets; ws = await websockets.connect("wss://host/ws/mobile/chat/123/?device_id=abc123")'
            },
            'error_codes': {
                '4001': 'Missing device_id parameter',
                '4002': 'Invalid or inactive device_id',
                '4003': 'Conversation not found',
                '4004': 'Access denied (conversation does not belong to device)'
            },
            'documentation': 'See WEBSOCKET_CHAT_ENDPOINT.md for complete documentation with examples'
        }, status=status.HTTP_200_OK)



class MobileFacilityViewSet(viewsets.ViewSet):
    """
    Mobile Facility API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_facilities_list",
        operation_description="List facilities optimized for mobile app with pagination support. Facilities are automatically sorted by distance (closest first) when GPS coordinates are available in the mobile session. If no GPS is available, facilities are sorted alphabetically.",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'service_category', openapi.IN_QUERY, description="Service category filter", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'constituency', openapi.IN_QUERY, description="Filter by constituency ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'ward', openapi.IN_QUERY, description="Filter by ward ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'radius_km', openapi.IN_QUERY, description="Filter facilities within radius (km) using GPS from mobile session", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number (default: 1)", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Items per page (default: 100, max: 500)", type=openapi.TYPE_INTEGER, required=False
            )
        ],
        responses={
            200: openapi.Response('Facilities list with pagination', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of facilities'),
                    'next': openapi.Schema(type=openapi.TYPE_STRING, description='URL for next page', nullable=True),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING, description='URL for previous page', nullable=True),
                    'results': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT), description='List of facilities')
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Facility API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_facilities(self, request):
        """List facilities optimized for mobile app with pagination and location-based sorting"""
        from django.db.models import F, FloatField
        from django.db.models.functions import Power, Sqrt
        
        # Get mobile session (already validated by permission class)
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        search_query = request.query_params.get('search', '')
        service_category = request.query_params.get('service_category', '')
        county_id = request.query_params.get('county')  # Optional county filter
        constituency_id = request.query_params.get('constituency')  # Optional constituency filter
        ward_id = request.query_params.get('ward')  # Optional ward filter
        radius_km = request.query_params.get('radius_km')  # Optional radius filter
        
        # Pagination parameters
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
        except ValueError:
            page = 1
            page_size = 100
        
        # Enforce reasonable limits
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 100
        if page_size > 500:
            page_size = 500  # Max 500 per page to prevent performance issues
        
        queryset = Facility.objects.filter(is_active=True)
        
        # Apply location filters if provided
        if county_id:
            queryset = queryset.filter(ward__constituency__county_id=county_id)
        
        if constituency_id:
            queryset = queryset.filter(ward__constituency_id=constituency_id)
        
        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)
        
        if search_query:
            queryset = queryset.filter(
                Q(facility_name__icontains=search_query) |
                Q(ward__ward_name__icontains=search_query) |
                Q(ward__constituency__constituency_name__icontains=search_query) |
                Q(ward__constituency__county__county_name__icontains=search_query)
            )
        
        if service_category:
            queryset = queryset.filter(
                facilityservice__service_category__category_name__icontains=service_category
            )
        
        # Location-based sorting using mobile session GPS
        latitude = None
        longitude = None
        use_distance = False
        
        # Get GPS from mobile session if available
        if mobile_session.latitude and mobile_session.longitude:
            latitude = float(mobile_session.latitude)
            longitude = float(mobile_session.longitude)
            use_distance = True
        
        # Handle radius filtering if specified
        radius_km_float = None
        if radius_km:
            try:
                radius_km_float = float(radius_km)
                if not latitude or not longitude:
                    return Response(
                        {'error': 'GPS coordinates required for radius filtering. Please ensure your mobile session has location data.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Invalid radius_km value. Must be a number.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Calculate distance and sort by closest if GPS is available
        if use_distance and latitude and longitude:
            # Filter only facilities with coordinates for distance-based sorting
            # This ensures we only show facilities we can calculate distance for
            queryset = queryset.filter(
                facilitycoordinate__latitude__isnull=False,
                facilitycoordinate__longitude__isnull=False,
                facilitycoordinate__is_active=True
            )
            
            # Annotate with distance using Haversine approximation
            queryset = queryset.annotate(
                distance_km=Sqrt(
                    Power(F('facilitycoordinate__latitude') - latitude, 2) +
                    Power(F('facilitycoordinate__longitude') - longitude, 2),
                    output_field=FloatField()
                ) * 111.32  # Approximate conversion to km
            )
            
            # Apply radius filter if specified
            if radius_km_float:
                queryset = queryset.filter(distance_km__lte=radius_km_float)
            
            # Order by distance (closest first), then by facility name
            queryset = queryset.order_by('distance_km', 'facility_name')
        else:
            # No GPS available - will order by facility_id after distinct()
            pass
        
        # Apply distinct to avoid duplicates from joins
        queryset = queryset.distinct()
        
        # Apply ordering AFTER distinct() to ensure it's preserved
        if use_distance and latitude and longitude and radius_km_float:
            # Already ordered by distance above
            pass
        elif use_distance and latitude and longitude:
            # Already ordered by distance above
            pass
        else:
            # No GPS - order by facility_id DESCENDING (newest first) to avoid Baringo bias
            # This shows most recently added facilities first, which avoids alphabetical/default ordering
            queryset = queryset.order_by('-facility_id')
        
        # Get total count before pagination
        total_count = queryset.count()
        
        # Optimize for mobile with select_related and prefetch_related
        # Use Prefetch to filter active items and reduce data transfer
        from django.db.models import Prefetch
        
        # Optimize prefetch based on query type
        if use_distance and latitude and longitude:
            # For distance queries, coordinates are already filtered in the main query
            # Use lightweight prefetch to minimize data transfer
            queryset = queryset.select_related(
                'ward', 'ward__constituency', 'ward__constituency__county',
                'operational_status'
            ).prefetch_related(
                # Only prefetch minimal service/contact data for counts
                Prefetch(
                    'facilityservice_set',
                    queryset=FacilityService.objects.filter(is_active=True).only('is_active'),
                    to_attr='_prefetched_services'
                ),
                Prefetch(
                    'facilitycontact_set',
                    queryset=FacilityContact.objects.filter(is_active=True).only('is_active'),
                    to_attr='_prefetched_contacts'
                )
            )
        else:
            # For non-distance queries, prefetch coordinates too
            queryset = queryset.select_related(
                'ward', 'ward__constituency', 'ward__constituency__county',
                'operational_status'
            ).prefetch_related(
                # Prefetch only active coordinates (first one for list view)
                Prefetch(
                    'facilitycoordinate_set',
                    queryset=FacilityCoordinate.objects.filter(
                        is_active=True,
                        latitude__isnull=False,
                        longitude__isnull=False
                    ).only('latitude', 'longitude', 'is_active').order_by('-created_at')[:1],
                    to_attr='_prefetched_coord_list'
                ),
                # Prefetch only active services (lightweight)
                Prefetch(
                    'facilityservice_set',
                    queryset=FacilityService.objects.filter(is_active=True).only('is_active'),
                    to_attr='_prefetched_services'
                ),
                # Prefetch only active contacts (lightweight)
                Prefetch(
                    'facilitycontact_set',
                    queryset=FacilityContact.objects.filter(is_active=True).only('is_active'),
                    to_attr='_prefetched_contacts'
                )
            )
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        
        # Attach first coordinate to each facility for serializer access
        # For distance queries, coordinates are already joined in the query
        # For non-distance queries, we prefetched them
        if not (use_distance and latitude and longitude):
            # Attach prefetched coordinates
            for facility in paginated_queryset:
                if hasattr(facility, '_prefetched_coord_list') and facility._prefetched_coord_list:
                    facility._prefetched_coord = facility._prefetched_coord_list[0]
        # For distance queries, coordinates are accessible via the relationship
        # The serializer will handle fetching them if needed
        
        # Use lightweight serializer for list view (much faster - ~70% smaller payload)
        serializer = MobileAppFacilityListSerializer(paginated_queryset, many=True, context={'request': request})
        
        # Add distance information to response if available
        response_data = serializer.data
        if use_distance and latitude and longitude:
            for i, facility_data in enumerate(response_data):
                if hasattr(paginated_queryset[i], 'distance_km'):
                    try:
                        facility_data['distance_km'] = round(float(paginated_queryset[i].distance_km), 2)
                    except (ValueError, TypeError):
                        pass
        
        # Build pagination response
        base_url = request.build_absolute_uri(request.path)
        query_params = request.query_params.copy()
        
        # Calculate next and previous page URLs
        next_url = None
        previous_url = None
        
        if end < total_count:
            query_params['page'] = page + 1
            next_url = f"{base_url}?{query_params.urlencode()}"
        
        if page > 1:
            query_params['page'] = page - 1
            previous_url = f"{base_url}?{query_params.urlencode()}"
        
        # Build optimized response
        response = Response({
            'count': total_count,
            'next': next_url,
            'previous': previous_url,
            'results': response_data,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'location_aware': use_distance,
            'user_location': {
                'latitude': latitude,
                'longitude': longitude
            } if use_distance else None,
            'sorting_info': {
                'method': 'distance' if use_distance else 'facility_id_desc',
                'gps_available': use_distance,
                'message': 'Sorted by distance (closest first)' if use_distance else 'Sorted by facility ID (newest first) - GPS not available in mobile session'
            }
        })
        
        # Add cache headers for mobile optimization (short TTL for real-time data)
        # Cache for 30 seconds - balances performance with data freshness
        response['Cache-Control'] = 'public, max-age=30, s-maxage=30'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    
    @swagger_auto_schema(
        operation_id="mobile_facilities_map",
        operation_description="Get facilities with coordinates optimized for map display. Supports viewport-based loading for smooth performance. Returns minimal data (id, name, coordinates) for fast loading. This endpoint is optimized for mobile map rendering.",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'ne_lat', openapi.IN_QUERY, description="Northeast latitude for viewport filtering", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'ne_lng', openapi.IN_QUERY, description="Northeast longitude for viewport filtering", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'sw_lat', openapi.IN_QUERY, description="Southwest latitude for viewport filtering", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'sw_lng', openapi.IN_QUERY, description="Southwest longitude for viewport filtering", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'zoom', openapi.IN_QUERY, description="Map zoom level (1-20). Higher zoom = more facilities. Default: 10", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'constituency', openapi.IN_QUERY, description="Filter by constituency ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'ward', openapi.IN_QUERY, description="Filter by ward ID", type=openapi.TYPE_INTEGER, required=False
            ),
        ],
        responses={
            200: openapi.Response('Facilities for map display', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'facilities': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        description='List of facilities with coordinates'
                    ),
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of facilities returned'),
                    'viewport': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description='Viewport information if provided'
                    )
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Facility API"]
    )
    @action(detail=False, methods=['get'], url_path='map')
    def get_facilities_map(self, request):
        """Get facilities with coordinates optimized for map display - viewport-based loading"""
        from django.db.models import Prefetch
        
        # Get mobile session (already validated by permission class)
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        # Get viewport parameters for efficient loading
        ne_lat = request.query_params.get('ne_lat')
        ne_lng = request.query_params.get('ne_lng')
        sw_lat = request.query_params.get('sw_lat')
        sw_lng = request.query_params.get('sw_lng')
        zoom_level = request.query_params.get('zoom', 10)
        
        try:
            zoom_level = int(zoom_level)
            if zoom_level < 1:
                zoom_level = 1
            if zoom_level > 20:
                zoom_level = 20
        except (ValueError, TypeError):
            zoom_level = 10
        
        # Base queryset - only facilities with active coordinates
        queryset = Facility.objects.filter(
            is_active=True,
            facilitycoordinate__latitude__isnull=False,
            facilitycoordinate__longitude__isnull=False,
            facilitycoordinate__is_active=True
        )
        
        # Apply viewport filtering if provided (for dynamic loading)
        if ne_lat and ne_lng and sw_lat and sw_lng:
            try:
                ne_lat = float(ne_lat)
                ne_lng = float(ne_lng)
                sw_lat = float(sw_lat)
                sw_lng = float(sw_lng)
                
                # Handle longitude wrapping (e.g., crossing 180/-180)
                if sw_lng > ne_lng:
                    # Crosses the date line - use OR condition
                    queryset = queryset.filter(
                        facilitycoordinate__latitude__gte=sw_lat,
                        facilitycoordinate__latitude__lte=ne_lat
                    ).filter(
                        Q(facilitycoordinate__longitude__gte=sw_lng) |
                        Q(facilitycoordinate__longitude__lte=ne_lng)
                    )
                else:
                    # Normal case
                    queryset = queryset.filter(
                        facilitycoordinate__latitude__gte=sw_lat,
                        facilitycoordinate__latitude__lte=ne_lat,
                        facilitycoordinate__longitude__gte=sw_lng,
                        facilitycoordinate__longitude__lte=ne_lng
                    )
            except (ValueError, TypeError):
                # Invalid viewport parameters - ignore and return all
                pass
        
        # Apply location filters if provided
        county_id = request.query_params.get('county')
        if county_id:
            try:
                queryset = queryset.filter(ward__constituency__county_id=int(county_id))
            except (ValueError, TypeError):
                pass
        
        constituency_id = request.query_params.get('constituency')
        if constituency_id:
            try:
                queryset = queryset.filter(ward__constituency_id=int(constituency_id))
            except (ValueError, TypeError):
                pass
        
        ward_id = request.query_params.get('ward')
        if ward_id:
            try:
                queryset = queryset.filter(ward_id=int(ward_id))
            except (ValueError, TypeError):
                pass
        
        # Optimize query - only select what we need (BEFORE slicing)
        queryset = queryset.only(
            'facility_id', 'facility_name'
        ).prefetch_related(
            Prefetch(
                'facilitycoordinate_set',
                queryset=FacilityCoordinate.objects.filter(
                    is_active=True,
                    latitude__isnull=False,
                    longitude__isnull=False
                ).only('latitude', 'longitude', 'is_active').order_by('-created_at')[:1],
                to_attr='_prefetched_map_coord_list'
            )
        ).distinct()
        
        # Limit results based on zoom level for performance (AFTER distinct)
        # Higher zoom = more detail = more facilities
        if zoom_level <= 5:
            # Country level - show only operational facilities, limit to 500
            queryset = queryset.filter(
                operational_status__status_name='Operational'
            )[:500]
        elif zoom_level <= 8:
            # Regional level - show more facilities, limit to 2000
            queryset = queryset[:2000]
        elif zoom_level <= 12:
            # City level - show many facilities, limit to 5000
            queryset = queryset[:5000]
        else:
            # Street level - show all facilities in viewport, limit to 10000
            queryset = queryset[:10000]
        
        # Attach first coordinate to each facility for serializer access
        for facility in queryset:
            if hasattr(facility, '_prefetched_map_coord_list') and facility._prefetched_map_coord_list:
                facility._prefetched_map_coord = facility._prefetched_map_coord_list[0]
        
        # Use ultra-lightweight serializer for map
        serializer = MobileFacilityMapSerializer(queryset, many=True, context={'request': request})
        
        # Filter out facilities without coordinates
        facilities_data = [f for f in serializer.data if f.get('coordinates') is not None]
        
        # Build response
        response_data = {
            'facilities': facilities_data,
            'count': len(facilities_data),
        }
        
        # Add viewport info if provided
        if ne_lat and ne_lng and sw_lat and sw_lng:
            response_data['viewport'] = {
                'ne_lat': float(ne_lat),
                'ne_lng': float(ne_lng),
                'sw_lat': float(sw_lat),
                'sw_lng': float(sw_lng),
                'zoom': zoom_level
            }
        
        response = Response(response_data)
        
        # Add cache headers for mobile optimization (short TTL for real-time data)
        # Cache for 60 seconds - balances performance with data freshness for maps
        response['Cache-Control'] = 'public, max-age=60, s-maxage=60'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    
    @swagger_auto_schema(
        operation_id="mobile_facility_detail",
        operation_description="Get facility details optimized for mobile app",
        responses={
            200: openapi.Response('Facility details', MobileAppFacilitySerializer),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Facility API"]
    )
    @action(detail=True, methods=['get'], url_path='detail')
    def get_facility_detail(self, request, pk=None):
        """Get facility details optimized for mobile app"""
        facility = get_object_or_404(Facility, facility_id=pk, is_active=True)
        serializer = MobileAppFacilitySerializer(facility, context={'request': request})
        return Response(serializer.data)


class MobileSessionViewSet(viewsets.ViewSet):
    """
    Mobile Session API endpoints
    """
    
    permission_classes = []  # No authentication required for session creation
    # Ensure API responses are JSON (avoid HTML error pages)
    renderer_classes = [JSONRenderer]
    
    @swagger_auto_schema(
        operation_id="mobile_session_create",
        operation_description="Create a new mobile session or retrieve existing one",
        request_body=MobileSessionCreateSerializer,
        responses={
            200: openapi.Response('Existing session retrieved', MobileSessionSerializer),
            201: openapi.Response('New session created', MobileSessionSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Session API"]
    )
    @action(detail=False, methods=['post'], url_path='create')
    def create_session(self, request):
        """Create a new mobile session or retrieve existing one"""
        serializer = MobileSessionCreateSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            
            # Check if session already exists for this device
            try:
                existing_session = MobileSession.objects.get(device_id=device_id)
                
                # If session exists but is inactive, reactivate it
                if not existing_session.is_active:
                    existing_session.is_active = True
                    existing_session.last_active_at = timezone.now()
                    existing_session.save(update_fields=['is_active', 'last_active_at', 'updated_at'])
                
                # Update session properties if provided
                update_fields = ['updated_at']
                if serializer.validated_data.get('notification_enabled') is not None:
                    existing_session.notification_enabled = serializer.validated_data['notification_enabled']
                    update_fields.append('notification_enabled')
                if serializer.validated_data.get('dark_mode_enabled') is not None:
                    existing_session.dark_mode_enabled = serializer.validated_data['dark_mode_enabled']
                    update_fields.append('dark_mode_enabled')
                if serializer.validated_data.get('preferred_language'):
                    existing_session.preferred_language = serializer.validated_data['preferred_language']
                    update_fields.append('preferred_language')
                if serializer.validated_data.get('location_data'):
                    location_data = serializer.validated_data['location_data']
                    if 'latitude' in location_data and 'longitude' in location_data:
                        existing_session.latitude = location_data['latitude']
                        existing_session.longitude = location_data['longitude']
                        existing_session.location_updated_at = timezone.now()
                        update_fields.extend(['latitude', 'longitude', 'location_updated_at'])
                
                existing_session.save(update_fields=update_fields)
                session = existing_session
                
                response_serializer = MobileSessionSerializer(session, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_200_OK)
                
            except MobileSession.DoesNotExist:
                # Create new session if none exists
                session = MobileSessionService.create_session(
                    device_id=device_id,
                    device_info=serializer.validated_data.get('device_info', {}),
                    location_data=serializer.validated_data.get('location_data', {})
                )
                
                response_serializer = MobileSessionSerializer(session, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """GET /mobile/sessions/?device_id=... -> return session JSON or 404 JSON

        The mobile client calls GET /mobile/sessions/?device_id=... to retrieve an
        existing session. Return 200 with session JSON when found, or 404 JSON
        when not found (client will create a new session).
        """
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({'error': 'Missing device_id', 'message': 'device_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = MobileSession.objects.get(device_id=device_id)
            serializer = MobileSessionSerializer(session, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MobileSession.DoesNotExist:
            return Response({'error': 'Not Found', 'message': f'Session not found for device ID: {device_id}'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_id="mobile_session_end",
        operation_description="End a mobile session - only requires device_id",
        request_body=MobileSessionEndSerializer,
        responses={
            200: openapi.Response('Session ended', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'device_id': openapi.Schema(type=openapi.TYPE_STRING)
            })),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Session API"]
    )
    @action(detail=False, methods=['post'], url_path='end')
    def end_session(self, request):
        """End a mobile session"""
        serializer = MobileSessionEndSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            
            try:
                session = MobileSession.objects.get(device_id=device_id, is_active=True)
                session = MobileSessionService.end_session(session)
                
                return Response({
                    'message': 'Session ended successfully',
                    'device_id': session.device_id
                })
                
            except MobileSession.DoesNotExist:
                return Response(
                    {'error': 'Session not found or already inactive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id="mobile_session_update",
        operation_description="Update mobile session properties",
        request_body=MobileSessionUpdateSerializer,
        responses={
            200: openapi.Response('Session updated', MobileSessionSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Session API"]
    )
    @action(detail=False, methods=['put'], url_path='update')
    def update_session(self, request):
        """Update mobile session properties"""
        serializer = MobileSessionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            
            try:
                session = MobileSession.objects.get(device_id=device_id, is_active=True)
                
                # Update only the fields that were provided
                update_fields = ['updated_at']
                for field, value in serializer.validated_data.items():
                    if field != 'device_id' and hasattr(session, field):
                        setattr(session, field, value)
                        update_fields.append(field)
                
                session.save(update_fields=update_fields)
                
                response_serializer = MobileSessionSerializer(session, context={'request': request})
                return Response(response_serializer.data)
                
            except MobileSession.DoesNotExist:
                return Response(
                    {'error': 'Session not found or inactive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MobileMusicViewSet(viewsets.ViewSet):
    """
    Mobile Music API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_music_list",
        operation_description="List music tracks for mobile app with pagination support",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'artist', openapi.IN_QUERY, description="Filter by artist", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number (default: 1)", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Items per page (default: 100, max: 500)", type=openapi.TYPE_INTEGER, required=False
            )
        ],
        responses={
            200: openapi.Response('Music list with pagination', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of tracks'),
                    'next': openapi.Schema(type=openapi.TYPE_STRING, description='URL for next page', nullable=True),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING, description='URL for previous page', nullable=True),
                    'results': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT), description='List of music tracks')
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Music API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_music(self, request):
        """List music tracks for mobile app with pagination"""
        # Use query_params if available (DRF), otherwise fall back to GET (Django)
        query_params = getattr(request, 'query_params', request.GET)
        
        genre = query_params.get('genre', '')
        artist = query_params.get('artist', '')
        
        # Pagination parameters
        try:
            page = int(query_params.get('page', 1))
            page_size = int(query_params.get('page_size', 100))
        except ValueError:
            page = 1
            page_size = 100
        
        # Enforce reasonable limits
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 100
        if page_size > 500:
            page_size = 500  # Max 500 per page
        
        # Optimize query - only fetch needed fields for list view
        queryset = Music.objects.filter(is_active=True).only(
            'music_id', 'name', 'description', 'link', 'music_file',
            'artist', 'duration', 'genre', 'is_active', 'created_at'
        )
        
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        if artist:
            queryset = queryset.filter(artist__icontains=artist)
        
        # Get total count before pagination (optimized)
        total_count = queryset.count()
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        
        serializer = MusicSerializer(paginated_queryset, many=True, context={'request': request})
        
        # Ensure music file URLs are absolute and accessible for mobile
        music_data = serializer.data
        scheme = 'https' if request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https' else 'http'
        host = request.get_host()
        file_base_url = f"{scheme}://{host}"
        
        for track in music_data:
            if track.get('music_file') and not track['music_file'].startswith('http'):
                # Make URL absolute
                track['music_file'] = file_base_url + track['music_file']
            if track.get('link'):
                # External link is already absolute
                pass
        
        # Build pagination response
        base_url = request.build_absolute_uri(request.path)
        from urllib.parse import urlencode
        
        # Calculate next and previous page URLs
        next_url = None
        previous_url = None
        
        if end < total_count:
            next_params = request.query_params.copy()
            next_params['page'] = page + 1
            next_url = f"{base_url}?{urlencode(next_params)}"
        
        if page > 1:
            prev_params = request.query_params.copy()
            prev_params['page'] = page - 1
            previous_url = f"{base_url}?{urlencode(prev_params)}"
        
        # Build optimized response with cache headers
        response = Response({
            'count': total_count,
            'next': next_url,
            'previous': previous_url,
            'results': music_data,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        })
        
        # Add cache headers for mobile optimization (60 seconds for music - less frequently updated)
        response['Cache-Control'] = 'public, max-age=60, s-maxage=60'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response


class MobileDocumentViewSet(viewsets.ViewSet):
    """
    Mobile Document API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    # Force JSON responses for API clients (avoid HTML error pages)
    renderer_classes = [JSONRenderer]
    
    @swagger_auto_schema(
        operation_id="mobile_documents_list",
        operation_description="List documents for mobile app",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'document_type', openapi.IN_QUERY, description="Filter by document type", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Documents list', DocumentSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Document API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_documents(self, request):
        """List documents for mobile app"""
        # Required: device_id (mobile client relies on it)
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response({'error': 'Missing device_id', 'message': 'device_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filters
        document_type = request.query_params.get('document_type')
        gbv_category = request.query_params.get('gbv_category')
        is_public = request.query_params.get('is_public')

        # Pagination
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
        except ValueError:
            page = 1
            page_size = 100

        # Enforce reasonable limits
        if page_size < 1:
            page_size = 100
        if page_size > 500:
            page_size = 500

        # Optimize query - only fetch needed fields for list view
        queryset = Document.objects.filter(is_active=True).select_related(
            'document_type', 'gbv_category'
        ).only(
            'document_id', 'title', 'description', 'file_url', 'file_name',
    'file_size_bytes', 'document_type', 'gbv_category', 'is_public',
    'is_active', 'uploaded_at')


        # Filter by is_public if provided (accept 'true'/'false' case-insensitive)
        if is_public is not None:
            is_public_str = str(is_public).lower()
            if is_public_str in ['true', '1', 'yes']:
                queryset = queryset.filter(is_public=True)
            elif is_public_str in ['false', '0', 'no']:
                queryset = queryset.filter(is_public=False)

        # Filter by document_type (expecting int id)
        if document_type:
            try:
                dt = int(document_type)
                queryset = queryset.filter(document_type__document_type_id=dt)
            except Exception:
                # fallback: try matching by name
                queryset = queryset.filter(document_type__type_name__icontains=document_type)

        # Filter by gbv_category (expecting int id)
        if gbv_category:
            try:
                gc = int(gbv_category)
                queryset = queryset.filter(gbv_category__gbv_category_id=gc)
            except Exception:
                # fallback: try matching by name
                queryset = queryset.filter(gbv_category__category_name__icontains=gbv_category)

        # Ordering: newest first
        queryset = queryset.order_by('-uploaded_at')

        # Simple pagination (client only needs list; meta optional)
        start = (page - 1) * page_size
        end = start + page_size
        paged_qs = queryset[start:end]

        serializer = DocumentSerializer(paged_qs, many=True, context={'request': request})
        
        # Ensure file URLs are absolute and accessible for mobile
        doc_data = serializer.data
        scheme = 'https' if request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https' else 'http'
        host = request.get_host()
        base_url = f"{scheme}://{host}"
        
        for doc in doc_data:
            # Priority: file_url > file > external_url
            if doc.get('file_url') and doc['file_url'].strip():
                if not doc['file_url'].startswith('http'):
                    # Make URL absolute
                    doc['file_url'] = base_url + doc['file_url']
            elif doc.get('file') and doc['file'].strip():
                if not doc['file'].startswith('http'):
                    doc['file_url'] = base_url + doc['file']
                else:
                    doc['file_url'] = doc['file']
            elif doc.get('external_url') and doc['external_url'].strip():
                # Use external_url as accessible URL for external documents
                doc['file_url'] = doc['external_url']
                doc['is_external'] = True

        # Build optimized response with cache headers
        response = Response({'results': doc_data}, status=status.HTTP_200_OK)
        
        # Add cache headers for mobile optimization (120 seconds for documents - rarely change)
        response['Cache-Control'] = 'public, max-age=120, s-maxage=120'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response

    # Provide a standard `list` method so DefaultRouter exposes `/mobile/documents/`.
    # The mobile client currently calls `/mobile/documents/` (no `/list/`) which returned 404.
    # This method delegates to `list_documents` so both `/mobile/documents/` and
    # `/mobile/documents/list/` behave the same.
    def list(self, request):
        """Compatibility wrapper: map default list route to list_documents action."""
        return self.list_documents(request)


class MobileEmergencyViewSet(viewsets.ViewSet):
    """
    Mobile Emergency API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_emergency_sos",
        operation_description="Send emergency SOS - location data is automatically retrieved from device session",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'emergency_type', openapi.IN_QUERY, description="Type of emergency", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            200: openapi.Response('Emergency SOS sent', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'emergency_type': openapi.Schema(type=openapi.TYPE_STRING),
                'location': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER)
                }),
                'facilities_nearby': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
            })),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Emergency API"]
    )
    @action(detail=False, methods=['post'], url_path='sos')
    def send_emergency_sos(self, request):
        """Send emergency SOS - location data is automatically retrieved from device session"""
        emergency_type = request.data.get('emergency_type')
        
        if not emergency_type:
            return Response(
                {'error': 'Missing required parameter: emergency_type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get location from the mobile session (already validated by permission class)
        mobile_session = request.mobile_session
        latitude = mobile_session.latitude
        longitude = mobile_session.longitude
        
        # Check if location data is available
        if latitude is None or longitude is None:
            return Response(
                {'error': 'Device location not available. Please enable location services and update location first.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find nearby facilities based on emergency type
        nearby_facilities = Facility.objects.filter(
            is_active=True,
            facilityservice__service_category__category_name__icontains=emergency_type
        )[:5]  # Limit to 5 closest facilities
        
        return Response({
            'message': 'Emergency SOS received',
            'emergency_type': emergency_type,
            'location': {'latitude': float(latitude), 'longitude': float(longitude)},
            'facilities_nearby': [
                {
                    'facility_id': facility.facility_id,
                    'facility_name': facility.facility_name,
                    'distance': 'Nearby'  # Simplified for now
                }
                for facility in nearby_facilities
            ]
        })


class MobileLookupViewSet(viewsets.ViewSet):
    """
    Mobile Lookup API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_lookups_data",
        operation_description="Get lookup data for mobile app",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'lookup_type', openapi.IN_QUERY, description="Type of lookup data", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Lookup data', openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Lookup API"]
    )
    @action(detail=False, methods=['get'], url_path='data')
    def get_lookup_data(self, request):
        """Get lookup data for mobile app"""
        lookup_type = request.query_params.get('lookup_type', '')
        
        if lookup_type == 'service_categories':
            data = ServiceCategory.objects.all().values('service_category_id', 'category_name', 'description', 'icon_url')
        elif lookup_type == 'gbv_categories':
            data = GBVCategory.objects.all().values('gbv_category_id', 'category_name', 'description', 'icon_url')
        elif lookup_type == 'contact_types':
            data = ContactType.objects.all().values('contact_type_id', 'type_name', 'validation_regex')
        else:
            # Return all lookup data
            data = {
                'service_categories': list(ServiceCategory.objects.all().values('service_category_id', 'category_name', 'description', 'icon_url')),
                'gbv_categories': list(GBVCategory.objects.all().values('gbv_category_id', 'category_name', 'description', 'icon_url')),
                'contact_types': list(ContactType.objects.all().values('contact_type_id', 'type_name', 'validation_regex')),
                'owner_types': list(OwnerType.objects.all().values('owner_type_id', 'type_name', 'description')),
                'infrastructure_types': list(InfrastructureType.objects.all().values('infrastructure_type_id', 'type_name', 'description')),
                'condition_statuses': list(ConditionStatus.objects.all().values('condition_status_id', 'status_name', 'description')),
                'document_types': list(DocumentType.objects.all().values('document_type_id', 'type_name', 'allowed_extensions', 'max_file_size_mb', 'description'))
            }
        
        return Response(data)


class MobileAnalyticsViewSet(viewsets.ViewSet):
    """
    Mobile Analytics API endpoints
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_analytics_contact_interaction",
        operation_description="Track contact interaction for analytics",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['facility_id', 'contact_type'],
            properties={
                'facility_id': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="ID of the facility for the interaction",
                    example="FAC001"
                ),
                'contact_type': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="Type of contact interaction (e.g., phone, email, visit)",
                    example="phone"
                ),
                'interaction_data': openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    description="Additional data about the interaction",
                    example={},
                    default={}
                )
            }
        ),
        responses={
            200: openapi.Response('Interaction tracked', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'interaction_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            })),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Analytics API"]
    )
    @action(detail=False, methods=['post'], url_path='contact-interaction')
    def track_contact_interaction(self, request):
        """Track contact interaction for analytics"""
        facility_id = request.data.get('facility_id')
        contact_type = request.data.get('contact_type')
        interaction_data = request.data.get('interaction_data', {})
        
        if not all([facility_id, contact_type]):
            return Response(
                {'error': 'Missing required parameters: facility_id, contact_type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            facility = Facility.objects.get(facility_id=facility_id, is_active=True)
            
            # Find the specific contact for this facility and contact type
            try:
                facility_contact = FacilityContact.objects.get(
                    facility=facility,
                    contact_type__type_name__iexact=contact_type,
                    is_active=True
                )
            except FacilityContact.DoesNotExist:
                return Response(
                    {'error': f'Contact of type "{contact_type}" not found for facility {facility_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create contact interaction record
            interaction = ContactInteraction.objects.create(
                contact=facility_contact,
                device=request.mobile_session,
                user_latitude=request.mobile_session.latitude,
                user_longitude=request.mobile_session.longitude,
                is_helpful=interaction_data.get('is_helpful'),
                interaction_type='general',
                click_data=interaction_data,
                created_at=timezone.now()
            )
            
            return Response({
                'message': 'Contact interaction tracked successfully',
                'interaction_id': interaction.interaction_id,
                'contact_id': facility_contact.contact_id,
                'facility_name': facility.facility_name,
                'contact_type': contact_type,
                'contact_value': facility_contact.contact_value
            })
            
        except Facility.DoesNotExist:
            return Response(
                {'error': 'Facility not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to track interaction: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_id="mobile_analytics_contact_click",
        operation_description="Track when a user clicks on a specific contact (e.g., phone number, email)",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['contact_id'],
            properties={
                'contact_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description="ID of the specific contact that was clicked",
                    example=123
                ),
                'click_type': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="Type of click action (e.g., 'call', 'email', 'sms', 'whatsapp')",
                    example="call",
                    default="click"
                ),
                'click_data': openapi.Schema(
                    type=openapi.TYPE_OBJECT, 
                    description="Additional data about the click",
                    example={
                        "duration": 30,
                        "successful": True,
                        "notes": "User called the facility"
                    },
                    default={}
                )
            }
        ),
        responses={
            200: openapi.Response('Contact click tracked', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'interaction_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'contact_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'facility_name': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_type': openapi.Schema(type=openapi.TYPE_STRING),
                'contact_value': openapi.Schema(type=openapi.TYPE_STRING)
            })),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Contact not found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Analytics API"]
    )
    @action(detail=False, methods=['post'], url_path='contact-click')
    def track_contact_click(self, request):
        """Track when a user clicks on a specific contact"""
        contact_id = request.data.get('contact_id')
        click_type = request.data.get('click_type', 'click')
        click_data = request.data.get('click_data', {})
        
        if not contact_id:
            return Response(
                {'error': 'Missing required parameter: contact_id'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get the specific contact
            facility_contact = FacilityContact.objects.get(
                contact_id=contact_id,
                is_active=True
            )
            
            # Create contact interaction record for the click
            interaction = ContactInteraction.objects.create(
                contact=facility_contact,
                device=request.mobile_session,
                user_latitude=request.mobile_session.latitude,
                user_longitude=request.mobile_session.longitude,
                is_helpful=click_data.get('is_helpful'),
                interaction_type=click_type,
                click_data=click_data,
                created_at=timezone.now()
            )
            
            return Response({
                'message': 'Contact click tracked successfully',
                'interaction_id': interaction.interaction_id,
                'contact_id': facility_contact.contact_id,
                'facility_name': facility_contact.facility.facility_name,
                'contact_type': facility_contact.contact_type.type_name,
                'contact_value': facility_contact.contact_value,
                'click_type': click_type,
                'click_data': click_data
            })
            
        except FacilityContact.DoesNotExist:
            return Response(
                {'error': 'Contact not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to track contact click: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class MobileResourcesViewSet(viewsets.ViewSet):
    """
    Mobile Resources API endpoints
    Consolidated endpoint for all mobile resources (documents, music, etc.)
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_resources_list",
        operation_description="Get all resources (documents, music) for mobile app in a single consolidated response",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'resource_type', openapi.IN_QUERY, description="Filter by resource type: 'documents', 'music', or 'all' (default: 'all')", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number (default: 1)", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Items per page (default: 50, max: 200)", type=openapi.TYPE_INTEGER, required=False
            )
        ],
        responses={
            200: openapi.Response('Resources list', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'documents': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'results': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                        }
                    ),
                    'music': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'results': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                        }
                    ),
                    'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total resources across all types')
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Resources API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def get_resources(self, request):
        """Get all resources (documents, music) for mobile app with accessible file URLs"""
        from rest_framework.pagination import PageNumberPagination
        from django.conf import settings
        
        # Get mobile session (already validated by permission class)
        # Check if mobile_session exists (set by MobileSessionPermission)
        if hasattr(request, 'mobile_session') and request.mobile_session:
            mobile_session = request.mobile_session
            mobile_session.update_activity()
        
        resource_type = request.query_params.get('resource_type', 'all').lower()
        try:
            page = int(request.query_params.get('page', 1))
            page_size = min(int(request.query_params.get('page_size', 50)), 200)
        except (ValueError, TypeError):
            page = 1
            page_size = 50
        
        response_data = {
            'total_count': 0
        }
        
        # Get base URL for file serving
        scheme = 'https' if request.is_secure() or request.META.get('HTTP_X_FORWARDED_PROTO') == 'https' else 'http'
        host = request.get_host()
        base_url = f"{scheme}://{host}"
        
        # Get documents if requested
        if resource_type in ['all', 'documents']:
            documents = Document.objects.filter(is_active=True).order_by('-uploaded_at')
            doc_paginator = PageNumberPagination()
            doc_paginator.page_size = page_size
            doc_page = doc_paginator.paginate_queryset(documents, request)
            doc_serializer = DocumentSerializer(doc_page, many=True, context={'request': request}) if doc_page else DocumentSerializer([], many=True)
            
            # Ensure file URLs are absolute and accessible
            doc_data = doc_serializer.data
            for doc in doc_data:
                # Priority: file_url > file > external_url
                if doc.get('file_url') and doc['file_url'].strip():
                    if not doc['file_url'].startswith('http'):
                        # Make URL absolute
                        doc['file_url'] = base_url + doc['file_url']
                elif doc.get('file') and doc['file'].strip():
                    if not doc['file'].startswith('http'):
                        doc['file_url'] = base_url + doc['file']
                    else:
                        doc['file_url'] = doc['file']
                elif doc.get('external_url') and doc['external_url'].strip():
                    # Use external_url as accessible URL for external documents
                    doc['file_url'] = doc['external_url']
                    doc['is_external'] = True
            
            response_data['documents'] = {
                'count': documents.count(),
                'results': doc_data
            }
            response_data['total_count'] += documents.count()
        else:
            response_data['documents'] = {'count': 0, 'results': []}
        
        # Get music if requested
        if resource_type in ['all', 'music']:
            music = Music.objects.filter(is_active=True).order_by('-created_at')  # Music has created_at
            music_paginator = PageNumberPagination()
            music_paginator.page_size = page_size
            music_page = music_paginator.paginate_queryset(music, request)
            music_serializer = MusicSerializer(music_page, many=True, context={'request': request}) if music_page else MusicSerializer([], many=True)
            
            # Ensure music file URLs are absolute and accessible
            music_data = music_serializer.data
            for track in music_data:
                if track.get('music_file') and not track['music_file'].startswith('http'):
                    # Make URL absolute
                    track['music_file'] = base_url + track['music_file']
                if track.get('link'):
                    # External link is already absolute
                    pass
            
            response_data['music'] = {
                'count': music.count(),
                'results': music_data
            }
            response_data['total_count'] += music.count()
        else:
            response_data['music'] = {'count': 0, 'results': []}
        
        response = Response(response_data)
        response['Cache-Control'] = 'public, max-age=300, s-maxage=300'
        return response


class MobileContactViewSet(viewsets.ViewSet):
    """
    Mobile Contact API endpoints
    
    Provides access to facility contacts with location-based filtering and search capabilities.
    """
    
    permission_classes = [MobileSessionPermission]
    
    @swagger_auto_schema(
        operation_id="mobile_contacts_list",
        operation_description="List facility contacts with filtering, search, and location-based sorting",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID from mobile session", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'contact_type', openapi.IN_QUERY, description="Filter by contact type (e.g., Phone, Email)", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'facility_id', openapi.IN_QUERY, description="Filter by facility ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'county', openapi.IN_QUERY, description="Filter by county ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'constituency', openapi.IN_QUERY, description="Filter by constituency ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'ward', openapi.IN_QUERY, description="Filter by ward ID", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search in contact value, person name, or facility name", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'radius_km', openapi.IN_QUERY, description="Filter contacts within radius (km) using GPS from mobile session", type=openapi.TYPE_NUMBER, required=False
            ),
            openapi.Parameter(
                'primary_only', openapi.IN_QUERY, description="Show only primary contacts", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number (default: 1)", type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Items per page (default: 100, max: 500)", type=openapi.TYPE_INTEGER, required=False
            )
        ],
        responses={
            200: openapi.Response('Contacts list with pagination', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of contacts'),
                    'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current page number'),
                    'page_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Items per page'),
                    'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of pages'),
                    'next': openapi.Schema(type=openapi.TYPE_STRING, description='URL for next page', nullable=True),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING, description='URL for previous page', nullable=True),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                        description='List of contacts with facility and location information'
                    )
                }
            )),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            401: openapi.Response('Unauthorized - Invalid or inactive mobile session', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Contact API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_contacts(self, request):
        """List facility contacts with filtering, search, and location-based sorting"""
        from django.db.models import F, FloatField
        from django.db.models.functions import Power, Sqrt
        
        # Get mobile session (already validated by permission class)
        mobile_session = request.mobile_session
        mobile_session.update_activity()
        
        # Get filter parameters
        contact_type = request.query_params.get('contact_type', '').strip()
        facility_id = request.query_params.get('facility_id')
        county_id = request.query_params.get('county')
        constituency_id = request.query_params.get('constituency')
        ward_id = request.query_params.get('ward')
        search_query = request.query_params.get('search', '').strip()
        radius_km = request.query_params.get('radius_km')
        primary_only = request.query_params.get('primary_only', 'false').lower() == 'true'
        
        # Pagination parameters
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
        except ValueError:
            page = 1
            page_size = 100
        
        # Enforce reasonable limits
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 100
        if page_size > 500:
            page_size = 500
        
        # Start with active contacts from active facilities
        queryset = FacilityContact.objects.filter(
            is_active=True,
            facility__is_active=True
        ).select_related(
            'facility', 'facility__ward', 'facility__ward__constituency', 
            'facility__ward__constituency__county', 'contact_type'
        )
        
        # Apply filters
        if contact_type:
            queryset = queryset.filter(contact_type__type_name__icontains=contact_type)
        
        if facility_id:
            try:
                queryset = queryset.filter(facility_id=int(facility_id))
            except ValueError:
                pass
        
        if county_id:
            try:
                queryset = queryset.filter(facility__ward__constituency__county_id=int(county_id))
            except ValueError:
                pass
        
        if constituency_id:
            try:
                queryset = queryset.filter(facility__ward__constituency_id=int(constituency_id))
            except ValueError:
                pass
        
        if ward_id:
            try:
                queryset = queryset.filter(facility__ward_id=int(ward_id))
            except ValueError:
                pass
        
        if primary_only:
            queryset = queryset.filter(is_primary=True)
        
        if search_query:
            queryset = queryset.filter(
                Q(contact_value__icontains=search_query) |
                Q(contact_person_name__icontains=search_query) |
                Q(facility__facility_name__icontains=search_query)
            )
        
        # Location-based filtering and distance calculation
        latitude = None
        longitude = None
        use_distance = False
        
        # Get GPS from mobile session if available
        if mobile_session.latitude and mobile_session.longitude:
            latitude = float(mobile_session.latitude)
            longitude = float(mobile_session.longitude)
            use_distance = True
        
        # If radius is specified, we need GPS coordinates
        radius_km_float = None
        if radius_km:
            try:
                radius_km_float = float(radius_km)
                if not latitude or not longitude:
                    return Response(
                        {'error': 'GPS coordinates required for radius filtering. Please ensure your mobile session has location data.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Invalid radius_km value. Must be a number.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Calculate distance if GPS is available AND radius is specified
        if use_distance and latitude and longitude and radius_km_float:
            # Filter only facilities with coordinates when radius filtering is requested
            queryset = queryset.filter(
                facility__facilitycoordinate__latitude__isnull=False,
                facility__facilitycoordinate__longitude__isnull=False,
                facility__facilitycoordinate__is_active=True
            )
            
            # Annotate with distance using Haversine approximation
            queryset = queryset.annotate(
                distance_km=Sqrt(
                    Power(F('facility__facilitycoordinate__latitude') - latitude, 2) +
                    Power(F('facility__facilitycoordinate__longitude') - longitude, 2),
                    output_field=FloatField()
                ) * 111.32  # Approximate conversion to km
            )
            
            # Apply radius filter
            queryset = queryset.filter(distance_km__lte=radius_km_float)
            
            # Order by distance (nearest first)
            queryset = queryset.order_by('distance_km', 'facility__facility_name', 'contact_id')
        else:
            # No radius filtering - return all contacts, order alphabetically
            queryset = queryset.order_by('facility__facility_name', 'contact_type__type_name', 'contact_id')
        
        # Get total count before pagination
        total_count = queryset.count()
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        
        # Build response data
        results = []
        for contact in paginated_queryset:
            # Get facility coordinates if available
            facility_coords = None
            try:
                coord = contact.facility.facilitycoordinate_set.filter(is_active=True).first()
                if coord:
                    facility_coords = {
                        'latitude': float(coord.latitude),
                        'longitude': float(coord.longitude)
                    }
            except:
                pass
            
            contact_data = {
                'contact_id': contact.contact_id,
                'facility_id': contact.facility.facility_id,
                'facility_name': contact.facility.facility_name,
                'facility_registration_number': contact.facility.registration_number,
                'contact_type': contact.contact_type.type_name,
                'contact_value': contact.contact_value,
                'contact_person_name': contact.contact_person_name or '',
                'is_primary': contact.is_primary,
                'location': {
                    'ward': contact.facility.ward.ward_name,
                    'ward_id': contact.facility.ward.ward_id,
                    'constituency': contact.facility.ward.constituency.constituency_name,
                    'constituency_id': contact.facility.ward.constituency.constituency_id,
                    'county': contact.facility.ward.constituency.county.county_name,
                    'county_id': contact.facility.ward.constituency.county.county_id,
                },
                'coordinates': facility_coords,
            }
            
            # Add distance if calculated (only when radius filtering was used)
            if use_distance and radius_km_float and hasattr(contact, 'distance_km'):
                try:
                    contact_data['distance_km'] = round(float(contact.distance_km), 2)
                except (ValueError, TypeError):
                    pass
            
            results.append(contact_data)
        
        # Build pagination URLs
        base_url = request.build_absolute_uri(request.path)
        query_params = request.query_params.copy()
        
        next_url = None
        previous_url = None
        
        if end < total_count:
            query_params['page'] = page + 1
            next_url = f"{base_url}?{query_params.urlencode()}"
        
        if page > 1:
            query_params['page'] = page - 1
            previous_url = f"{base_url}?{query_params.urlencode()}"
        
        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'next': next_url,
            'previous': previous_url,
            'results': results,
            'filters_applied': {
                'contact_type': contact_type if contact_type else None,
                'facility_id': int(facility_id) if facility_id else None,
                'county_id': int(county_id) if county_id else None,
                'constituency_id': int(constituency_id) if constituency_id else None,
                'ward_id': int(ward_id) if ward_id else None,
                'search': search_query if search_query else None,
                'radius_km': radius_km_float if radius_km_float else None,
                'primary_only': primary_only,
                'location_aware': use_distance,
            }
        })


class MobileAiViewSet(viewsets.ViewSet):
    """
    Mobile AI assistant proxy.

    The app used to hold the Gemini API key and call Google directly, so the
    secret shipped inside the APK where anyone could extract it. The key now
    lives only on this server: quota and billing sit with GVRC in one place,
    and the prompt can be corrected without a new app release.
    """

    permission_classes = [MobileSessionPermission]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        operation_id="mobile_ai_chat",
        operation_description=(
            "Generate an assistant reply. The server holds the model key, "
            "composes the safety prompt, and applies model fallback."
        ),
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID",
                type=openapi.TYPE_STRING, required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['message'],
            properties={
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The user's message"),
                'history': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="Recent turns: [{role, content}, ...]",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                'facility_context': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=(
                        "Facts the app looked up in its facility cache. The "
                        "model is instructed to use only these for facility "
                        "questions.")),
            },
        ),
        responses={
            200: openapi.Response('Assistant reply'),
            400: openapi.Response('Bad Request'),
        },
        tags=["Mobile AI API"]
    )
    @action(detail=False, methods=['post'], url_path='chat')
    def chat(self, request):
        message = (request.data.get('message') or '').strip()
        if not message:
            return Response(
                {'error': 'message is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(message) > 4000:
            message = message[:4000]

        history = request.data.get('history') or []
        if not isinstance(history, list):
            history = []

        facility_context = request.data.get('facility_context') or ''
        if len(facility_context) > 4000:
            facility_context = facility_context[:4000]

        reply, meta = generate_reply(
            user_message=message,
            history=history,
            grounding_context=facility_context,
        )

        # Always 200 with a usable reply: the app shows what comes back, and
        # an assistant outage must not surface as an error screen to someone
        # who may be in distress.
        return Response({
            'reply': reply,
            'ok': meta.get('ok', False),
            'model': meta.get('model'),
        })



class MobileDirectionsViewSet(viewsets.ViewSet):
    """
    Road routing, proxied so the Maps web-service key stays on the server.

    The app shipped this key inside the APK. Anyone could unzip a release and
    spend GVRC's Maps budget, and rotating it meant shipping a new version to
    every handset. Routing now goes through here; the app holds no Maps
    credential for web services at all.
    """

    permission_classes = [MobileSessionPermission]
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(
        operation_id="mobile_directions_route",
        operation_description=(
            "Road route between two points. The server holds the Maps key. "
            "Returns the encoded overview polyline plus distance and duration "
            "text; the full upstream response is deliberately not forwarded."
        ),
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'origin', openapi.IN_QUERY, description="lat,lng",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'destination', openapi.IN_QUERY, description="lat,lng",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'mode', openapi.IN_QUERY,
                description="driving | walking | bicycling | transit",
                type=openapi.TYPE_STRING, required=False
            ),
        ],
        tags=["Mobile Directions API"]
    )
    @action(detail=False, methods=['get'], url_path='route')
    def route(self, request):
        payload, meta = directions_route(
            origin=request.query_params.get('origin'),
            destination=request.query_params.get('destination'),
            mode=request.query_params.get('mode'),
        )

        if not meta.get('ok'):
            # 200 with ok:false, matching the AI proxy. The caller draws a
            # straight line when routing is unavailable, which is a degraded
            # map rather than a failed screen.
            return Response({'ok': False, 'reason': meta.get('reason')})

        return Response({
            'ok': True,
            'polyline': payload['polyline'],
            'distance_text': payload['distance_text'],
            'duration_text': payload['duration_text'],
        })
