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
from apps.facilities.models import Facility, FacilityContact, FacilityService
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
    MobileAppFacilitySerializer, MusicSerializer, DocumentSerializer,
    MobileSessionSerializer, MobileSessionCreateSerializer, MobileSessionUpdateSerializer, MobileSessionEndSerializer
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
    
    def _send_message_auto_create(self, request):
        """Send a message with automatic conversation creation if needed"""
        device_id = self._get_request_device_id(request)
        
        # For superadmin users, device_id is optional but they need to specify a mobile session
        if request.user and request.user.is_authenticated and request.user.is_superuser:
            if not device_id:
                return Response(
                    {'error': 'device_id is required for auto-conversation creation, even for superadmin users'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if not device_id:
            return Response(
                {'error': 'device_id is required for mobile users'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session, error_message = self._validate_mobile_session(device_id)
        if not session:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
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
                # Auto-create conversation with smart subject generation
                conversation = ConversationService.get_or_create_conversation(
                    session, 
                    auto_generate_subject=True, 
                    first_message=content
                )
                
                # Auto-assign admin if this is a new conversation
                if conversation.status == 'new':
                    ConversationService.auto_assign_conversation(conversation)
                
                # Create the message
                message = MessageService.create_mobile_message(
                    conversation=conversation,
                    content=content,
                    message_type=message_type,
                    media_file=media_file,
                    media_url=media_url,
                    is_urgent=is_urgent,
                    metadata=metadata
                )
                
                # Return both message and conversation info
                message_serializer = MessageSerializer(message, context={'request': request})
                conversation_serializer = ConversationSerializer(conversation, context={'request': request})
                
                return Response({
                    'message': message_serializer.data,
                    'conversation': conversation_serializer.data,
                    'auto_created': True
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to create message/conversation: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        operation_id="mobile_chat_get_or_create",
        operation_description="Get existing conversation or create one automatically without requiring topic input. Perfect for seamless chat experience.",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID - required for mobile users", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            200: openapi.Response('Existing conversation retrieved', ConversationSerializer),
            201: openapi.Response('New conversation auto-created', ConversationSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Chat APIs"]
    )
    @action(detail=False, methods=['get'], url_path='get-or-create')
    def get_or_create_conversation(self, request):
        """Get existing conversation or automatically create one without topic input"""
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response(
                {'error': 'device_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            mobile_session = MobileSession.objects.get(device_id=device_id, is_active=True)
            
            # Check if there's already an open conversation for this device
            existing_conversation = Conversation.objects.filter(
                mobile_session=mobile_session,
                status__in=['new', 'active']
            ).order_by('-created_at').first()
            
            if existing_conversation:
                # Return existing conversation
                serializer = ConversationSerializer(existing_conversation, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # No conversation exists, create one automatically
            try:
                conversation = ConversationService.get_or_create_conversation(
                    mobile_session, 
                    auto_generate_subject=True
                )
                
                # Auto-assign admin for new conversations
                if conversation.status == 'new':
                    ConversationService.auto_assign_conversation(conversation)
                
                serializer = ConversationSerializer(conversation, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
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
        operation_description="Send a message in a conversation via REST API. Use conversation_id='auto' to automatically create a conversation if none exists. Requires device_id for mobile users. For real-time messaging, use the WebSocket endpoint: ws://host/ws/mobile/chat/{conversation_id}/?device_id=xxx",
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
        # Handle special case where pk="auto" - auto-create conversation if needed
        if pk == "auto":
            return self._send_message_auto_create(request)
        
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
        operation_description="List facilities optimized for mobile app",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'service_category', openapi.IN_QUERY, description="Service category filter", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Facilities list', MobileAppFacilitySerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Facility API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_facilities(self, request):
        """List facilities optimized for mobile app"""
        search_query = request.query_params.get('search', '')
        service_category = request.query_params.get('service_category', '')
        
        queryset = Facility.objects.filter(is_active=True)
        
        if search_query:
            queryset = queryset.filter(
                Q(facility_name__icontains=search_query) |
                Q(ward__ward_name__icontains=search_query) |
                Q(ward__constituency__constituency_name__icontains=search_query)
            )
        
        if service_category:
            queryset = queryset.filter(
                facilityservice__service_category__category_name__icontains=service_category
            )
        
        # Optimize for mobile with select_related and prefetch_related
        queryset = queryset.select_related(
            'ward', 'ward__constituency', 'ward__constituency__county'
        ).prefetch_related(
            'facilityservice_set__service_category',
            'facilitycontact_set__contact_type'
        )[:50]  # Limit results for mobile
        
        serializer = MobileAppFacilitySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
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
        operation_description="List music tracks for mobile app",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'genre', openapi.IN_QUERY, description="Filter by genre", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'artist', openapi.IN_QUERY, description="Filter by artist", type=openapi.TYPE_STRING, required=False
            )
        ],
        responses={
            200: openapi.Response('Music list', MusicSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile Music API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_music(self, request):
        """List music tracks for mobile app"""
        genre = request.query_params.get('genre', '')
        artist = request.query_params.get('artist', '')
        
        queryset = Music.objects.filter(is_active=True)
        
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        if artist:
            queryset = queryset.filter(artist__icontains=artist)
        
        serializer = MusicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


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
            page_size = int(request.query_params.get('page_size', 20))
        except ValueError:
            page = 1
            page_size = 20

        # Enforce reasonable limits
        if page_size < 1:
            page_size = 20
        if page_size > 100:
            page_size = 100

        queryset = Document.objects.filter(is_active=True)

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
        paged_qs = list(queryset[start:end])

        serializer = DocumentSerializer(paged_qs, many=True, context={'request': request})

        # Return results in a shape the client accepts
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

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
