# -*- encoding: utf-8 -*-
"""
Emergency Chat System API Views
"""

import logging

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q, Count
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Conversation, Message, ChatNotification
from .serializers import (
    ConversationSerializer, ConversationDetailSerializer, MessageSerializer,
    CreateConversationSerializer, CreateMessageSerializer, UpdateMessageStatusSerializer,
    ConversationAssignmentSerializer, ConversationStatusSerializer, ChatNotificationSerializer,
    MobileConversationListSerializer, AdminConversationListSerializer, ConversationStatsSerializer
)
from .services import (
    ConversationService, MessageService, NotificationService
)
from apps.mobile_sessions.models import MobileSession
from apps.authentication.models import User


logger = logging.getLogger(__name__)


class IsStaffUser(permissions.BasePermission):
    """Custom permission to only allow staff users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class MobileConversationViewSet(viewsets.ViewSet):
    """
    Mobile API endpoints for conversations
    
    Mobile users can:
    - Start/retrieve conversations
    - Send messages
    - Update message status
    - View conversation history
    """
    
    permission_classes = []  # No authentication required for mobile users
    
    def list(self, request, *args, **kwargs):
        """Router entry point for listing conversations"""
        return self.list_conversations(request)

    def create(self, request, *args, **kwargs):
        """Router entry point for creating a conversation"""
        return self.start_conversation(request)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """Router entry point for retrieving a conversation"""
        return self.get_conversation_detail(request, pk=pk)

    @swagger_auto_schema(
        operation_id="mobile_conversations_create",
        operation_description="Start a new conversation or retrieve existing one",
        request_body=CreateConversationSerializer,
        responses={
            200: openapi.Response('Conversation data', ConversationSerializer),
            201: openapi.Response('Conversation created', ConversationSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile API"]
    )
    @action(detail=False, methods=['post'], url_path='start')
    def start_conversation(self, request):
        """Start a new conversation or retrieve existing one"""
        serializer = CreateConversationSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            subject = serializer.validated_data.get('subject', '')
            
            try:
                mobile_session = MobileSession.objects.get(device_id=device_id, is_active=True)
                conversation = ConversationService.get_or_create_conversation(mobile_session, subject)
                
                # If new conversation, auto-assign admin
                if conversation.status == 'new':
                    ConversationService.auto_assign_conversation(conversation)
                
                response_serializer = ConversationSerializer(conversation, context={'request': request})
                
                if conversation.status == 'new':
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                    
            except MobileSession.DoesNotExist:
                return Response(
                    {'error': 'Invalid or inactive device ID'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as exc:
                logger.exception("Failed to start conversation for device %s", device_id)
                return Response(
                    {
                        'error': 'Failed to start conversation',
                        'detail': str(exc)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_id="mobile_conversations_list",
        operation_description="List conversations for a mobile device",
        manual_parameters=[
            openapi.Parameter(
                'device_id', openapi.IN_QUERY, description="Device ID", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            200: openapi.Response('Conversation list', MobileConversationListSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_conversations(self, request):
        """List conversations for a mobile device"""
        device_id = request.query_params.get('device_id')
        if not device_id:
            return Response(
                {'error': 'device_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            mobile_session = MobileSession.objects.get(device_id=device_id, is_active=True)
            conversations = Conversation.objects.filter(mobile_session=mobile_session).order_by('-last_message_at')
            
            serializer = MobileConversationListSerializer(conversations, many=True, context={'request': request})
            return Response(serializer.data)
            
        except MobileSession.DoesNotExist:
            return Response(
                {'error': 'Invalid or inactive device ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as exc:
            logger.exception("Failed to list conversations for device %s", device_id)
            return Response(
                {
                    'error': 'Failed to list conversations',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="mobile_conversations_detail",
        operation_description="Get conversation details with messages",
        manual_parameters=[
            openapi.Parameter(
                'limit', openapi.IN_QUERY, description="Number of messages to return", type=openapi.TYPE_INTEGER, default=50
            ),
            openapi.Parameter(
                'offset', openapi.IN_QUERY, description="Number of messages to skip", type=openapi.TYPE_INTEGER, default=0
            )
        ],
        responses={
            200: openapi.Response('Conversation details', ConversationDetailSerializer),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile API"]
    )
    @action(detail=True, methods=['get'], url_path='detail')
    def get_conversation_detail(self, request, pk=None):
        """Get conversation details with messages"""
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            serializer = ConversationDetailSerializer(conversation, context={'request': request})
            return Response(serializer.data)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to get conversation detail for %s", pk)
            return Response(
                {
                    'error': 'Failed to fetch conversation details',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="mobile_messages_create",
        operation_description="Send a message in a conversation",
        request_body=CreateMessageSerializer,
        responses={
            201: MessageSerializer,
            400: "Bad Request",
            404: "Not Found"
        },
        tags=["Mobile API"]
    )
    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """Send a message in a conversation"""
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            
            serializer = CreateMessageSerializer(data=request.data)
            if serializer.is_valid():
                message = MessageService.create_mobile_message(
                    conversation=conversation,
                    content=serializer.validated_data['content'],
                    message_type=serializer.validated_data['message_type'],
                    media_url=serializer.validated_data.get('media_url', ''),
                    is_urgent=serializer.validated_data.get('is_urgent', False),
                    metadata=serializer.validated_data.get('metadata', {})
                )
                
                response_serializer = MessageSerializer(message, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to send mobile message for conversation %s", pk)
            return Response(
                {
                    'error': 'Failed to send message',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="mobile_messages_status_update",
        operation_description="Update message delivery status",
        request_body=UpdateMessageStatusSerializer,
        responses={
            200: openapi.Response('Message updated', MessageSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Mobile API"]
    )
    @action(detail=False, methods=['put'], url_path='messages/(?P<message_id>[^/.]+)/status')
    def update_message_status(self, request, message_id=None):
        """Update message delivery status"""
        try:
            message = get_object_or_404(Message, message_id=message_id)
            
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
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to update message status for %s", message_id)
            return Response(
                {
                    'error': 'Failed to update message status',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminConversationViewSet(viewsets.ViewSet):
    """
    Admin API endpoints for conversations
    
    Admins can:
    - View all conversations
    - Assign conversations to themselves or others
    - Send messages
    - Update conversation status
    - View statistics
    """
    
    permission_classes = []  # No authentication required
    
    @swagger_auto_schema(
        operation_id="admin_conversations_list",
        operation_description="List all conversations with filtering options",
        manual_parameters=[
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING, 
                enum=['new', 'active', 'resolved', 'closed']
            ),
            openapi.Parameter(
                'priority', openapi.IN_QUERY, description="Filter by priority", type=openapi.TYPE_STRING,
                enum=['low', 'medium', 'high', 'urgent']
            ),
            openapi.Parameter(
                'assigned', openapi.IN_QUERY, description="Filter by assignment", type=openapi.TYPE_STRING,
                enum=['assigned', 'unassigned']
            )
        ],
        responses={
            200: openapi.Response('Conversation list', AdminConversationListSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    def list(self, request):
        """List all conversations with filtering options - this is the main endpoint"""
        queryset = Conversation.objects.all()
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        assigned_filter = request.query_params.get('assigned')
        if assigned_filter == 'assigned':
            queryset = queryset.filter(assigned_admin__isnull=False)
        elif assigned_filter == 'unassigned':
            queryset = queryset.filter(assigned_admin__isnull=True)
        
        # Handle admin filter (for unassigned conversations)
        admin_filter = request.query_params.get('admin')
        if admin_filter == 'unassigned':
            queryset = queryset.filter(assigned_admin__isnull=True)
        elif admin_filter and admin_filter != 'unassigned':
            queryset = queryset.filter(assigned_admin_id=admin_filter)
        
        # Handle search filter
        search_filter = request.query_params.get('search')
        if search_filter:
            queryset = queryset.filter(
                Q(subject__icontains=search_filter) |
                Q(mobile_session__device_id__icontains=search_filter) |
                Q(last_message__icontains=search_filter)
            )
        
        # Order by priority and recency
        queryset = queryset.order_by('-last_message_at', '-created_at')
        
        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        start = (page - 1) * page_size
        end = start + page_size
        
        conversations = queryset[start:end]
        
        serializer = AdminConversationListSerializer(conversations, many=True, context={'request': request})
        
        return Response({
            'results': serializer.data,
            'count': queryset.count(),
            'page': page,
            'page_size': page_size,
            'total_pages': (queryset.count() + page_size - 1) // page_size
        })
    
    def retrieve(self, request, pk=None):
        """Get conversation details - this is the main endpoint for single conversation"""
        conversation = get_object_or_404(Conversation, conversation_id=pk)
        serializer = ConversationDetailSerializer(conversation, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_id="admin_conversations_list_action",
        operation_description="List all conversations with filtering options (action endpoint)",
        manual_parameters=[
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by status", type=openapi.TYPE_STRING, 
                enum=['new', 'active', 'resolved', 'closed']
            ),
            openapi.Parameter(
                'priority', openapi.IN_QUERY, description="Filter by priority", type=openapi.TYPE_STRING,
                enum=['low', 'medium', 'high', 'urgent']
            ),
            openapi.Parameter(
                'assigned', openapi.IN_QUERY, description="Filter by assignment", type=openapi.TYPE_STRING,
                enum=['assigned', 'unassigned']
            )
        ],
        responses={
            200: openapi.Response('Conversation list', AdminConversationListSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['get'], url_path='list')
    def list_conversations(self, request):
        """List all conversations with filtering options"""
        queryset = Conversation.objects.all()
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        assigned_filter = request.query_params.get('assigned')
        if assigned_filter == 'assigned':
            queryset = queryset.filter(assigned_admin__isnull=False)
        elif assigned_filter == 'unassigned':
            queryset = queryset.filter(assigned_admin__isnull=True)
        
        # Order by priority and recency
        queryset = queryset.order_by('-priority', '-last_message_at', '-created_at')
        
        serializer = AdminConversationListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_id="admin_conversations_detail",
        operation_description="Get conversation details with messages",
        manual_parameters=[
            openapi.Parameter(
                'limit', openapi.IN_QUERY, description="Number of messages to return", type=openapi.TYPE_INTEGER, default=50
            ),
            openapi.Parameter(
                'offset', openapi.IN_QUERY, description="Number of messages to skip", type=openapi.TYPE_INTEGER, default=0
            )
        ],
        responses={
            200: openapi.Response('Conversation details', ConversationDetailSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['get'], url_path='detail')
    def get_conversation_detail(self, request, pk=None):
        """Get conversation details with messages"""
        conversation = get_object_or_404(Conversation, conversation_id=pk)
        serializer = ConversationDetailSerializer(conversation, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_id="admin_conversations_assign",
        operation_description="Assign conversation to an admin",
        request_body=ConversationAssignmentSerializer,
        responses={
            200: openapi.Response('Conversation assigned', ConversationSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['post'], url_path='assign')
    def assign_conversation(self, request, pk=None):
        """Assign conversation to an admin"""
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            
            serializer = ConversationAssignmentSerializer(data=request.data)
            if serializer.is_valid():
                admin_user_id = serializer.validated_data['admin_user_id']
                try:
                    admin_user = User.objects.get(user_id=admin_user_id)
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Admin user not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                conversation = ConversationService.assign_admin_to_conversation(conversation, admin_user)
                response_serializer = ConversationSerializer(conversation, context={'request': request})
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to assign conversation %s", pk)
            return Response(
                {
                    'error': 'Failed to assign conversation',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_conversations_status_update",
        operation_description="Update conversation status and priority",
        request_body=ConversationStatusSerializer,
        responses={
            200: openapi.Response('Conversation updated', ConversationSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['put'], url_path='status')
    def update_conversation_status(self, request, pk=None):
        """Update conversation status and priority"""
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            
            serializer = ConversationStatusSerializer(data=request.data)
            if serializer.is_valid():
                if 'status' in serializer.validated_data:
                    conversation.status = serializer.validated_data['status']
                
                if 'priority' in serializer.validated_data:
                    conversation.priority = serializer.validated_data['priority']
                
                conversation.save()
                
                response_serializer = ConversationSerializer(conversation, context={'request': request})
                return Response(response_serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to update conversation %s status", pk)
            return Response(
                {
                    'error': 'Failed to update conversation status',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_conversations_messages",
        operation_description="Get messages for a conversation",
        manual_parameters=[
            openapi.Parameter(
                'limit', openapi.IN_QUERY, description="Number of messages to return", type=openapi.TYPE_INTEGER, default=50
            ),
            openapi.Parameter(
                'offset', openapi.IN_QUERY, description="Number of messages to skip", type=openapi.TYPE_INTEGER, default=0
            ),
            openapi.Parameter(
                'after', openapi.IN_QUERY, description="Get messages after this ID", type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response('Messages list', MessageSerializer),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['get'], url_path='messages')
    def get_messages(self, request, pk=None):
        """Get messages for a conversation"""
        try:
            limit = int(request.query_params.get('limit', 50))
            offset = int(request.query_params.get('offset', 0))
        except ValueError:
            return Response(
                {'error': 'limit and offset must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            
            after_id = request.query_params.get('after')
            
            queryset = Message.objects.filter(conversation=conversation).order_by('sent_at')
            
            if after_id:
                queryset = queryset.filter(message_id__gt=after_id)
            
            messages = queryset[offset:offset + limit]
            
            # Debug information
            debug_info = {
                'conversation_id': pk,
                'total_messages_in_db': Message.objects.count(),
                'messages_for_conversation': queryset.count(),
                'limit': limit,
                'offset': offset,
                'actual_messages_returned': len(messages)
            }
            
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            return Response({
                'results': serializer.data,
                'count': queryset.count(),
                'limit': limit,
                'offset': offset,
                'debug': debug_info
            })
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to fetch messages for conversation %s", pk)
            return Response(
                {
                    'error': 'Failed to fetch messages',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_conversations_messages_create",
        operation_description="Send a message as admin",
        request_body=CreateMessageSerializer,
        responses={
            201: openapi.Response('Message sent', MessageSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['post'], url_path='send-message')
    def create_message(self, request, pk=None):
        """Send a message as admin"""
        try:
            conversation = get_object_or_404(Conversation, pk=pk)
            
            # Handle both form data (file uploads) and JSON data
            print(f"DEBUG: Request content type: {request.content_type}")
            print(f"DEBUG: Request data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'No keys'}")
            print(f"DEBUG: Request FILES keys: {list(request.FILES.keys()) if request.FILES else 'No FILES'}")
            
            # For file uploads, we need to merge request.FILES into request.data
            if request.content_type and 'multipart/form-data' in request.content_type:
                print(f"DEBUG: Using multipart form data")
                # Create a mutable copy of request.data and merge files
                data = request.data.copy()
                if request.FILES:
                    data.update(request.FILES)
                print(f"DEBUG: Merged data keys: {list(data.keys())}")
                serializer = CreateMessageSerializer(data=data)
            else:
                print(f"DEBUG: Using regular data")
                serializer = CreateMessageSerializer(data=request.data)
            
            if serializer.is_valid():
                # Get validated data
                content = serializer.validated_data.get('content', '')
                message_type = serializer.validated_data.get('message_type', 'text')
                media_file = serializer.validated_data.get('media_file')
                media_url = serializer.validated_data.get('media_url', '')
                is_urgent = serializer.validated_data.get('is_urgent', False)
                metadata = serializer.validated_data.get('metadata', {})
                
                print(f"DEBUG: After validation - media_file: {media_file}")
                if media_file:
                    print(f"DEBUG: media_file type: {type(media_file)}")
                    print(f"DEBUG: media_file name: {media_file.name}")
                    print(f"DEBUG: media_file size: {media_file.size}")
                
                # Determine message type based on file if not specified
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
                
                # Create message using service
                message = MessageService.create_message(
                    conversation=conversation,
                    content=content,
                    sender_type='admin',
                    sender=None,  # No specific user since we're not authenticated
                    message_type=message_type,
                    media_file=media_file,
                    media_url=media_url,
                    is_urgent=is_urgent,
                    metadata=metadata
                )
                
                response_serializer = MessageSerializer(message, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Add debugging information
            import traceback
            print(f"Error in create_message: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_id="admin_conversations_messages_read",
        operation_description="Mark messages as read",
        responses={
            200: openapi.Response('Messages marked as read', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['post'], url_path='messages/read')
    def mark_messages_read(self, request, pk=None):
        """Mark messages as read"""
        try:
            conversation = get_object_or_404(Conversation, pk=pk)
            
            # Mark all unread mobile messages as read
            unread_count = Message.objects.filter(
                conversation=conversation,
                sender_type='mobile',
                status__in=['sent', 'delivered']
            ).update(status='read', read_at=timezone.now())
            
            # Update conversation unread count
            conversation.unread_count_admin = 0
            conversation.save(update_fields=['unread_count_admin'])
            
            return Response({
                'message': 'Messages marked as read',
                'count': unread_count
            })
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to mark messages read for conversation %s", pk)
            return Response(
                {
                    'error': 'Failed to mark messages as read',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_conversations_resolve",
        operation_description="Mark conversation as resolved",
        responses={
            200: openapi.Response('Conversation resolved', ConversationSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve_conversation(self, request, pk=None):
        """Mark conversation as resolved"""
        try:
            conversation = get_object_or_404(Conversation, conversation_id=pk)
            conversation = ConversationService.mark_conversation_resolved(conversation)
            
            response_serializer = ConversationSerializer(conversation, context={'request': request})
            return Response(response_serializer.data)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to resolve conversation %s", pk)
            return Response(
                {
                    'error': 'Failed to resolve conversation',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_conversations_stats",
        operation_description="Get conversation statistics",
        responses={
            200: openapi.Response('Conversation statistics', ConversationStatsSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['get'], url_path='stats')
    def get_statistics(self, request):
        """Get conversation statistics"""
        stats = {
            'total_conversations': Conversation.objects.count(),
            'new_conversations': Conversation.objects.filter(status='new').count(),
            'active_conversations': Conversation.objects.filter(status='active').count(),
            'resolved_conversations': Conversation.objects.filter(status='resolved').count(),
            'unassigned_conversations': Conversation.objects.filter(assigned_admin__isnull=True).count(),
            'urgent_conversations': Conversation.objects.filter(priority='urgent').count(),
        }
        
        serializer = ConversationStatsSerializer(stats)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_id="admin_conversations_analytics",
        operation_description="Get detailed chat analytics and insights",
        manual_parameters=[
            openapi.Parameter(
                'time_range', openapi.IN_QUERY, description="Time range filter", type=openapi.TYPE_STRING,
                enum=['7d', '30d', '90d', '1y'], default='7d'
            ),
            openapi.Parameter(
                'start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response('Chat analytics data', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_conversations': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'active_conversations': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'avg_response_time': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'resolution_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'total_messages': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'mobile_messages': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'admin_messages': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'avg_messages_per_conversation': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'status_distribution': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'priority_distribution': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'conversations_trend_data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    'top_admins': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    'activity_hours': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                }
            )),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['get'], url_path='analytics')
    def get_analytics(self, request):
        """Get detailed chat analytics and insights"""
        try:
            from datetime import timedelta
            
            # Get time range parameters
            time_range = request.query_params.get('time_range', '7d')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # Set default dates if not provided
            if not start_date or not end_date:
                end_date = timezone.now().date()
                if time_range == '7d':
                    start_date = end_date - timedelta(days=7)
                elif time_range == '30d':
                    start_date = end_date - timedelta(days=30)
                elif time_range == '90d':
                    start_date = end_date - timedelta(days=90)
                else:
                    start_date = end_date - timedelta(days=7)
            else:
                # Convert string dates to date objects
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Convert to datetime for filtering
            start_datetime = timezone.make_aware(
                timezone.datetime.combine(start_date, timezone.datetime.min.time())
            )
            end_datetime = timezone.make_aware(
                timezone.datetime.combine(end_date, timezone.datetime.max.time())
            )
            
            # Get conversations in date range
            conversations = Conversation.objects.filter(
                created_at__range=(start_datetime, end_datetime)
            ).select_related('assigned_admin')
            
            # Calculate basic metrics
            total_conversations = conversations.count()
            
            if total_conversations == 0:
                # No data available - return empty response
                return Response({
                    'total_conversations': 0,
                    'active_conversations': 0,
                    'avg_response_time': 0,
                    'resolution_rate': 0,
                    'total_messages': 0,
                    'mobile_messages': 0,
                    'admin_messages': 0,
                    'avg_messages_per_conversation': 0,
                    'status_distribution': {},
                    'priority_distribution': {},
                    'conversations_trend_data': [],
                    'top_admins': [],
                    'activity_hours': [],
                })
            
            # Calculate status-based metrics
            active_conversations = conversations.filter(status='active').count()
            resolved_conversations = conversations.filter(status='resolved').count()
            
            # Calculate resolution rate
            resolution_rate = resolved_conversations / total_conversations if total_conversations > 0 else 0
            
            # Get messages in date range
            messages = Message.objects.filter(
                conversation__created_at__range=(start_datetime, end_datetime)
            )
            
            total_messages = messages.count()
            mobile_messages = messages.filter(sender_type='mobile').count()
            admin_messages = messages.filter(sender_type='admin').count()
            
            # Calculate average messages per conversation
            avg_messages_per_conversation = total_messages / total_conversations if total_conversations > 0 else 0
            
            # Calculate average response time (simplified - only for conversations with admin responses)
            conversations_with_admin_response = conversations.filter(
                messages__sender_type='admin'
            ).distinct()
            
            avg_response_time = 0
            if conversations_with_admin_response.exists():
                total_response_time = 0
                response_count = 0
                
                for conversation in conversations_with_admin_response:
                    first_admin_message = conversation.messages.filter(
                        sender_type='admin'
                    ).order_by('sent_at').first()
                    
                    if first_admin_message:
                        response_time = (first_admin_message.sent_at - conversation.created_at).total_seconds() / 60
                        total_response_time += response_time
                        response_count += 1
                
                if response_count > 0:
                    avg_response_time = round(total_response_time / response_count, 1)
            
            # Get status distribution
            status_distribution = {}
            if total_conversations > 0:
                status_counts = conversations.values('status').annotate(
                    count=Count('conversation_id')
                )
                status_distribution = {item['status']: item['count'] for item in status_counts}
            
            # Get priority distribution
            priority_distribution = {}
            if total_conversations > 0:
                priority_counts = conversations.values('priority').annotate(
                    count=Count('conversation_id')
                )
                priority_distribution = {item['priority']: item['count'] for item in priority_counts}
            
            # Get conversations trend data (daily) - only if meaningful
            conversations_trend = []
            if total_conversations > 0:
                current_date = start_date
                while current_date <= end_date:
                    daily_count = conversations.filter(
                        created_at__date=current_date
                    ).count()
                    conversations_trend.append({
                        'date': current_date.strftime('%b %d'),
                        'count': daily_count
                    })
                    current_date += timedelta(days=1)
            
            # Get top admin performers (only if there are assigned conversations)
            top_admins = []
            assigned_conversations = conversations.filter(assigned_admin__isnull=False)
            
            if assigned_conversations.exists():
                admin_stats = User.objects.filter(
                    is_staff=True,
                    assigned_conversations__created_at__range=(start_datetime, end_datetime)
                ).annotate(
                    conversations_handled=Count('assigned_conversations')
                ).filter(conversations_handled__gt=0).order_by('-conversations_handled')[:5]
                
                # Calculate average response time for each admin (simplified)
                for admin in admin_stats:
                    admin_conversations = admin.assigned_conversations.filter(
                        created_at__range=(start_datetime, end_datetime)
                    )
                    
                    admin_response_time = 0
                    response_count = 0
                    
                    for conversation in admin_conversations:
                        first_admin_message = conversation.messages.filter(
                            sender_type='admin'
                        ).order_by('sent_at').first()
                        
                        if first_admin_message:
                            response_time = (first_admin_message.sent_at - conversation.created_at).total_seconds() / 60
                            admin_response_time += response_time
                            response_count += 1
                    
                    if response_count > 0:
                        admin.avg_response_time = round(admin_response_time / response_count, 1)
                    else:
                        admin.avg_response_time = 0
                
                top_admins = [
                    {
                        'username': admin.username,
                        'conversations_handled': admin.conversations_handled,
                        'avg_response_time': admin.avg_response_time
                    }
                    for admin in admin_stats
                ]
            
            # Get activity hours (simplified - only if meaningful)
            activity_hours = []
            if total_conversations > 0:
                for hour in range(24):
                    hour_count = conversations.filter(
                        created_at__hour=hour
                    ).count()
                    if hour_count > 0:  # Only include hours with activity
                        activity_hours.append({
                            'hour': hour,
                            'count': hour_count
                        })
            
            # Prepare response data
            analytics_data = {
                'total_conversations': total_conversations,
                'active_conversations': active_conversations,
                'avg_response_time': avg_response_time,
                'resolution_rate': resolution_rate,
                'total_messages': total_messages,
                'mobile_messages': mobile_messages,
                'admin_messages': admin_messages,
                'avg_messages_per_conversation': round(avg_messages_per_conversation, 1),
                'status_distribution': status_distribution,
                'priority_distribution': priority_distribution,
                'conversations_trend_data': conversations_trend,
                'top_admins': top_admins,
                'activity_hours': activity_hours,
            }
            
            return Response(analytics_data)
        except Exception as exc:
            logger.exception("Failed to generate chat analytics")
            return Response(
                {
                    'error': 'Failed to generate chat analytics',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationViewSet(viewsets.ViewSet):
    """
    Notification management for admins
    """
    
    permission_classes = [IsStaffUser]
    
    @swagger_auto_schema(
        operation_id="admin_notifications_list",
        operation_description="Get unread notifications for admin",
        responses={
            200: openapi.Response('Notifications list', ChatNotificationSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['get'], url_path='unread')
    def list_unread(self, request):
        """Get unread notifications for admin"""
        try:
            notifications = NotificationService.get_unread_notifications(request.user)
            serializer = ChatNotificationSerializer(notifications, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as exc:
            logger.exception("Failed to list unread notifications for user %s", request.user)
            return Response(
                {
                    'error': 'Failed to fetch unread notifications',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_notifications_mark_read",
        operation_description="Mark notification as read",
        responses={
            200: openapi.Response('Notification marked as read', ChatNotificationSerializer),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Not Found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        try:
            notification = get_object_or_404(ChatNotification, notification_id=pk, user=request.user)
            notification = NotificationService.mark_notification_read(notification)
            
            serializer = ChatNotificationSerializer(notification, context={'request': request})
            return Response(serializer.data)
        except Http404:
            raise
        except Exception as exc:
            logger.exception("Failed to mark notification %s read for user %s", pk, request.user)
            return Response(
                {
                    'error': 'Failed to mark notification as read',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_notifications_mark_all_read",
        operation_description="Mark all notifications as read",
        responses={
            200: openapi.Response('All notifications marked as read', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        try:
            count = NotificationService.mark_all_notifications_read(request.user)
            return Response({
                'message': 'All notifications marked as read',
                'count': count
            })
        except Exception as exc:
            logger.exception("Failed to mark all notifications read for user %s", request.user)
            return Response(
                {
                    'error': 'Failed to mark notifications as read',
                    'detail': str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @swagger_auto_schema(
        operation_id="admin_notifications_unread_conversations",
        operation_description="Get unread conversations for notification dropdown",
        responses={
            200: openapi.Response('Unread conversations data', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'unread_conversations': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    'total_unread_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'unread_conversations_count': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )),
            403: openapi.Response('Forbidden', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}))
        },
        tags=["Admin API"]
    )
    @action(detail=False, methods=['get'], url_path='unread-conversations')
    def unread_conversations(self, request):
        """Get unread conversations for notification dropdown"""
        try:
            # Get unread conversations for admin
            unread_conversations = Conversation.objects.filter(
                unread_count_admin__gt=0
            ).select_related(
                'mobile_session', 'assigned_admin', 'last_message_by'
            ).order_by('-last_message_at')[:5]  # Limit to 5 most recent
            
            # Calculate total unread count
            total_unread_count = sum(conv.unread_count_admin for conv in unread_conversations)
            
            # Serialize conversations
            conversations_data = []
            for conv in unread_conversations:
                conversations_data.append({
                    'conversation_id': conv.conversation_id,
                    'subject': conv.subject,
                    'last_message': conv.last_message,
                    'last_message_at': conv.last_message_at,
                    'unread_count_admin': conv.unread_count_admin,
                    'priority': conv.priority,
                    'status': conv.status,
                    'device_id': conv.mobile_session.device_id if conv.mobile_session else 'Unknown',
                    'priority_display': conv.get_priority_display(),
                    'conversation_url': f"/chat/conversations/{conv.conversation_id}/"
                })
            
            return Response({
                'unread_conversations': conversations_data,
                'total_unread_count': total_unread_count,
                'unread_conversations_count': len(unread_conversations)
            })
        except Exception as e:
            logger.exception("Failed to fetch unread conversations for user %s", request.user)
            return Response({
                'error': 'Failed to fetch unread conversations',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)