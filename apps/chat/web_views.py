# -*- encoding: utf-8 -*-
"""
Emergency Chat System Web Views
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from datetime import timedelta
import json

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from apps.authentication.models import User
from apps.authentication.views import custom_login_required


def debug_auth(request):
    """Debug endpoint to check authentication status"""
    debug_info = {
        'user_authenticated': request.user.is_authenticated,
        'user_email': getattr(request.user, 'email', 'No user'),
        'user_id': getattr(request.user, 'user_id', 'No ID'),
        'is_staff': getattr(request.user, 'is_staff', False),
        'is_superuser': getattr(request.user, 'is_superuser', False),
        'is_active': getattr(request.user, 'is_active', False),
        'session_key': request.session.session_key if hasattr(request, 'session') else 'No session',
        'session_data': dict(request.session) if hasattr(request, 'session') else 'No session data',
        'request_path': request.path,
        'request_method': request.method,
        'request_headers': dict(request.headers),
    }
    return JsonResponse(debug_info)


def test_chat_access(request):
    """Simple test view to check if basic chat access works"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'User not staff'}, status=403)
    
    return JsonResponse({
        'success': True,
        'message': 'Chat access granted',
        'user': request.user.email,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser
    })


def is_staff_user(user):
    """Check if user is staff or superuser"""
    return user.is_staff or user.is_superuser


def conversation_list(request):
    """Display list of all conversations"""
    # Get filter parameters
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    admin = request.GET.get('admin', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    queryset = Conversation.objects.select_related(
        'mobile_session', 'assigned_admin', 'last_message_by'
    ).prefetch_related('messages').annotate(
        messages_count=Count('messages')
    ).order_by('-last_message_at', '-created_at')
    
    # Apply filters
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if admin == 'unassigned':
        queryset = queryset.filter(assigned_admin__isnull=True)
    elif admin:
        queryset = queryset.filter(assigned_admin_id=admin)
    if search:
        queryset = queryset.filter(
            Q(subject__icontains=search) |
            Q(mobile_session__device_id__icontains=search) |
            Q(last_message__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available admins for filter
    admins = User.objects.filter(is_staff=True).order_by('username')
    
    context = {
        'conversations': page_obj,
        'admins': admins,
        'segment': 'chat_conversations',
        'filters': {
            'status': status,
            'priority': priority,
            'admin': admin,
            'search': search,
        }
    }
    
    return render(request, 'chat/conversation_list.html', context)


def conversation_detail(request, conversation_id):
    """Display individual conversation with chat interface"""
    conversation = get_object_or_404(
        Conversation.objects.select_related(
            'mobile_session', 'assigned_admin', 'last_message_by'
        ),
        conversation_id=conversation_id
    )
    
    # Get messages for this conversation
    messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
    
    # Mark messages as read for this admin
    if conversation.assigned_admin == request.user:
        unread_messages = messages.filter(
            sender_type='mobile',
            status__in=['sent', 'delivered']
        )
        unread_messages.update(status='read', read_at=timezone.now())
        
        # Update conversation unread count
        conversation.unread_count_admin = 0
        conversation.save(update_fields=['unread_count_admin'])
    
    # Get all staff users for assignment dropdown
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admins = User.objects.filter(is_staff=True).exclude(user_id=request.user.user_id)
    
    # Serialize messages to include media_file_url
    from .serializers import MessageSerializer
    serialized_messages = MessageSerializer(messages, many=True, context={'request': request})
    
    context = {
        'conversation': conversation,
        'messages': serialized_messages.data,  # Use serialized data
        'admins': admins,
        'segment': 'chat_conversations',
    }
    
    return render(request, 'chat/conversation_detail.html', context)


def chat_analytics(request):
    """Display chat analytics and insights"""
    # Get time range parameters
    time_range = request.GET.get('time_range', '7d')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Set default dates if not provided
    if not start_date or not end_date:
        end_date = timezone.now().date()
        if time_range == '7d':
            start_date = end_date - timedelta(days=7)
        elif time_range == '30d':
            start_date = end_date - timedelta(days=30)
        elif time_range == '90d':
            start_date = end_date - timedelta(days=90)
        elif time_range == '1y':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=7)
    
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
    )
    
    # Calculate metrics
    total_conversations = conversations.count()
    active_conversations = conversations.filter(status='active').count()
    resolved_conversations = conversations.filter(status='resolved').count()
    
    # Calculate resolution rate
    resolution_rate = 0
    if total_conversations > 0:
        resolution_rate = resolved_conversations / total_conversations
    
    # Get messages in date range
    messages = Message.objects.filter(
        conversation__created_at__range=(start_datetime, end_datetime)
    )
    
    total_messages = messages.count()
    mobile_messages = messages.filter(sender_type='mobile').count()
    admin_messages = messages.filter(sender_type='admin').count()
    
    # Calculate average messages per conversation
    avg_messages_per_conversation = 0
    if total_conversations > 0:
        avg_messages_per_conversation = total_messages / total_conversations
    
    # Calculate overall average response time
    total_response_time = 0
    response_count = 0
    
    for conversation in conversations:
        # Get first admin message in each conversation
        first_admin_message = conversation.messages.filter(
            sender_type='admin'
        ).order_by('sent_at').first()
        
        if first_admin_message:
            # Calculate response time: first admin message time - conversation creation time
            response_time = (first_admin_message.sent_at - conversation.created_at).total_seconds() / 60  # in minutes
            total_response_time += response_time
            response_count += 1
    
    avg_response_time = 0
    if response_count > 0:
        avg_response_time = round(total_response_time / response_count, 1)
    
    # Get status distribution
    status_distribution = conversations.values('status').annotate(
        count=Count('conversation_id')
    ).order_by('status')
    
    # Get priority distribution
    priority_distribution = conversations.values('priority').annotate(
        count=Count('conversation_id')
    ).order_by('priority')
    
    # Get conversations trend data (daily)
    conversations_trend = []
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
    
    # Get top admin performers
    top_admins = User.objects.filter(
        is_staff=True,
        assigned_conversations__created_at__range=(start_datetime, end_datetime)
    ).annotate(
        conversations_handled=Count('assigned_conversations')
    ).order_by('-conversations_handled')[:5]
    
    # Calculate average response time for each admin
    for admin in top_admins:
        admin_conversations = admin.assigned_conversations.filter(
            created_at__range=(start_datetime, end_datetime)
        )
        
        total_response_time = 0
        response_count = 0
        
        for conversation in admin_conversations:
            # Get first admin message in each conversation
            first_admin_message = conversation.messages.filter(
                sender_type='admin'
            ).order_by('sent_at').first()
            
            if first_admin_message:
                # Calculate response time: first admin message time - conversation creation time
                response_time = (first_admin_message.sent_at - conversation.created_at).total_seconds() / 60  # in minutes
                total_response_time += response_time
                response_count += 1
        
        # Calculate average response time
        if response_count > 0:
            admin.avg_response_time = round(total_response_time / response_count, 1)
        else:
            admin.avg_response_time = 0
    
    # Get activity hours (simplified - just show distribution)
    activity_hours = []
    for hour in range(24):
        hour_count = conversations.filter(
            created_at__hour=hour
        ).count()
        activity_hours.append({
            'hour': hour,
            'count': hour_count
        })
    
    context = {
        'segment': 'chat_analytics',
        'analytics_data': {
            'total_conversations': total_conversations,
            'active_conversations': active_conversations,
            'resolution_rate': resolution_rate,
            'total_messages': total_messages,
            'mobile_messages': mobile_messages,
            'admin_messages': admin_messages,
            'avg_messages_per_conversation': avg_messages_per_conversation,
            'avg_response_time': avg_response_time, # Add overall average response time
            'status_distribution': {item['status']: item['count'] for item in status_distribution},
            'priority_distribution': {item['priority']: item['count'] for item in priority_distribution},
            'conversations_trend_data': conversations_trend,
            'top_admins': top_admins,
            'activity_hours': activity_hours,
        },
        'filters': {
            'time_range': time_range,
            'start_date': start_date,
            'end_date': end_date,
        }
    }
    
    return render(request, 'chat/chat_analytics.html', context)


def assign_conversation(request, conversation_id):
    """Assign conversation to admin"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
            
            if data.get('admin_id') == 'self':
                conversation.assigned_admin = request.user
                conversation.status = 'active'
                conversation.save()
                
                messages.success(request, f'Conversation assigned to you successfully.')
            else:
                admin_id = data.get('admin_id')
                if admin_id:
                    admin = get_object_or_404(User, user_id=admin_id, is_staff=True)
                    conversation.assigned_admin = admin
                    conversation.status = 'active'
                    conversation.save()
                    
                    messages.success(request, f'Conversation assigned to {admin.username} successfully.')
                else:
                    messages.error(request, 'Invalid admin ID provided.')
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def update_conversation_status(request, conversation_id):
    """Update conversation status"""
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
            
            new_status = data.get('status')
            if new_status in ['new', 'active', 'resolved', 'closed']:
                conversation.status = new_status
                conversation.save()
                
                messages.success(request, f'Conversation status updated to {new_status}.')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Invalid status provided'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def export_conversations(request):
    """Export conversations to CSV"""
    from django.http import HttpResponse
    import csv
    
    # Get filter parameters
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    admin = request.GET.get('admin', '')
    
    # Base queryset
    queryset = Conversation.objects.select_related(
        'mobile_session', 'assigned_admin'
    ).order_by('-created_at')
    
    # Apply filters
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if admin == 'unassigned':
        queryset = queryset.filter(assigned_admin__isnull=True)
    elif admin:
        queryset = queryset.filter(assigned_admin_id=admin)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="conversations.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Conversation ID',
        'Subject',
        'Status',
        'Priority',
        'Device ID',
        'Assigned Admin',
        'Created At',
        'Last Message At',
        'Messages Count'
    ])
    
    for conversation in queryset:
        writer.writerow([
            conversation.conversation_id,
            conversation.subject or 'Emergency Chat',
            conversation.status,
            conversation.priority,
            conversation.mobile_session.device_id,
            conversation.assigned_admin.username if conversation.assigned_admin else 'Unassigned',
            conversation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            conversation.last_message_at.strftime('%Y-%m-%d %H:%M:%S') if conversation.last_message_at else 'Never',
            conversation.messages.count()
        ])
    
    return response


def export_conversation(request, conversation_id):
    """Export individual conversation to CSV"""
    from django.http import HttpResponse
    import csv
    
    conversation = get_object_or_404(
        Conversation.objects.select_related('mobile_session', 'assigned_admin'),
        conversation_id=conversation_id
    )
    
    messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="conversation_{conversation_id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Conversation ID',
        'Subject',
        'Status',
        'Priority',
        'Device ID',
        'Assigned Admin',
        'Created At'
    ])
    
    writer.writerow([
        conversation.conversation_id,
        conversation.subject or 'Emergency Chat',
        conversation.status,
        conversation.priority,
        conversation.mobile_session.device_id,
        conversation.assigned_admin.username if conversation.assigned_admin else 'Unassigned',
        conversation.created_at.strftime('%Y-%m-%d %H:%M:%S')
    ])
    
    writer.writerow([])  # Empty row
    writer.writerow(['Messages'])
    writer.writerow([
        'Message ID',
        'Sender Type',
        'Content',
        'Sent At',
        'Status'
    ])
    
    for message in messages:
        writer.writerow([
            message.message_id,
            message.sender_type,
            message.content,
            message.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
            message.status
        ])
    
    return response


def export_analytics(request):
    """Export analytics data to CSV"""
    from django.http import HttpResponse
    import csv
    
    # Get time range parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        return JsonResponse({'error': 'Start and end dates are required'}, status=400)
    
    # Convert to datetime for filtering
    start_datetime = timezone.make_aware(
        timezone.datetime.combine(
            timezone.datetime.strptime(start_date, '%Y-%m-%d').date(),
            timezone.datetime.min.time()
        )
    )
    end_datetime = timezone.make_aware(
        timezone.datetime.combine(
            timezone.datetime.strptime(end_date, '%Y-%m-%d').date(),
            timezone.datetime.max.time()
        )
    )
    
    # Get conversations in date range
    conversations = Conversation.objects.filter(
        created_at__range=(start_datetime, end_datetime)
    )
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="chat_analytics_{start_date}_to_{end_date}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Chat Analytics Report'])
    writer.writerow([f'Period: {start_date} to {end_date}'])
    writer.writerow([])
    
    # Summary metrics
    total_conversations = conversations.count()
    active_conversations = conversations.filter(status='active').count()
    resolved_conversations = conversations.filter(status='resolved').count()
    
    writer.writerow(['Summary Metrics'])
    writer.writerow(['Total Conversations', total_conversations])
    writer.writerow(['Active Conversations', active_conversations])
    writer.writerow(['Resolved Conversations', resolved_conversations])
    writer.writerow(['Resolution Rate', f'{(resolved_conversations/total_conversations*100):.1f}%' if total_conversations > 0 else '0%'])
    writer.writerow([])
    
    # Status distribution
    writer.writerow(['Status Distribution'])
    status_distribution = conversations.values('status').annotate(
        count=Count('conversation_id')
    ).order_by('status')
    
    for item in status_distribution:
        writer.writerow([item['status'].title(), item['count']])
    writer.writerow([])
    
    # Priority distribution
    writer.writerow(['Priority Distribution'])
    priority_distribution = conversations.values('priority').annotate(
        count=Count('conversation_id')
    ).order_by('priority')
    
    for item in priority_distribution:
        writer.writerow([item['priority'].title(), item['count']])
    writer.writerow([])
    
    # Daily trends
    writer.writerow(['Daily Trends'])
    writer.writerow(['Date', 'Conversations'])
    
    current_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
    
    while current_date <= end_date_obj:
        daily_count = conversations.filter(created_at__date=current_date).count()
        writer.writerow([current_date.strftime('%Y-%m-%d'), daily_count])
        current_date += timedelta(days=1)
    
    return response


def debug_user_permissions(request):
    """Debug endpoint to check user authentication and permissions"""
    if request.user.is_authenticated:
        user_data = {
            'user_id': request.user.user_id,
            'email': request.user.email,
            'full_name': request.user.full_name,
            'is_authenticated': True,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'is_active': request.user.is_active,
            'verified': request.user.verified,
            'session_key': request.session.session_key if hasattr(request, 'session') else None,
            'has_perm_chat': request.user.has_perm('chat.view_conversation'),
            'has_perm_staff': request.user.has_perm('auth.view_user'),
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({
            'is_authenticated': False,
            'message': 'User not authenticated'
        })


def test_conversations_api(request):
    """Test endpoint to see if conversations can be loaded"""
    try:
        from .models import Conversation
        conversations = Conversation.objects.all()[:5]  # Get first 5 conversations
        
        data = {
            'success': True,
            'total_conversations': Conversation.objects.count(),
            'sample_conversations': []
        }
        
        for conv in conversations:
            data['sample_conversations'].append({
                'id': conv.conversation_id,
                'status': conv.status,
                'priority': conv.priority,
                'subject': conv.subject or 'No subject',
                'created_at': conv.created_at.isoformat() if conv.created_at else None,
                'assigned_admin': conv.assigned_admin.email if conv.assigned_admin else None
            })
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': str(e.__traceback__) if hasattr(e, '__traceback__') else 'No traceback'
        }, status=500)


def debug_messages(request, conversation_id):
    """Debug endpoint to check messages for a specific conversation"""
    try:
        from .models import Conversation, Message
        
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        messages = Message.objects.filter(conversation=conversation)
        
        data = {
            'success': True,
            'conversation_id': conversation_id,
            'conversation_status': conversation.status,
            'total_messages': messages.count(),
            'messages': []
        }
        
        for msg in messages[:10]:  # Get first 10 messages
            data['messages'].append({
                'id': msg.message_id,
                'content': msg.content[:100] + '...' if len(msg.content) > 100 else msg.content,
                'sender_type': msg.sender_type,
                'status': msg.status,
                'sent_at': msg.sent_at.isoformat() if msg.sent_at else None
            })
        
        return JsonResponse(data)
        
    except Conversation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Conversation {conversation_id} not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': str(e.__traceback__) if hasattr(e, '__traceback__') else 'No traceback'
        }, status=500)
