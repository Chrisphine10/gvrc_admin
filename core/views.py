#  apps/core/views.py (Views with caching and error handling)
# ============================================
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
import json
import logging
from .models import User, Post
from .utils import handle_errors, validate_json

logger = logging.getLogger('myproject')

@method_decorator(handle_errors, name='dispatch')
class UserListView(View):
    """User list view with caching and error handling"""
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request):
        try:
            page = request.GET.get('page', 1)
            per_page = min(int(request.GET.get('per_page', 10)), 100)  # Limit max per_page
            
            # Use optimized query with select_related and only()
            users = User.objects.select_related().filter(is_active=True).only(
                'id', 'username', 'email', 'first_name', 'last_name', 'created_at'
            )
            
            paginator = Paginator(users, per_page)
            page_obj = paginator.get_page(page)
            
            users_data = [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': f"{user.first_name} {user.last_name}",
                'created_at': user.created_at.isoformat()
            } for user in page_obj]
            
            logger.info(f'Users list retrieved - Page: {page}, Count: {len(users_data)}')
            
            return JsonResponse({
                'status': 'success',
                'data': users_data,
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                }
            })
            
        except Exception as e:
            logger.error(f'Error in UserListView: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to retrieve users'
            }, status=500)

    def post(self, request):
        try:
            data = validate_json(request.body)
            
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            
            logger.info(f'New user created: {user.username}')
            
            return JsonResponse({
                'status': 'success',
                'message': 'User created successfully',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except KeyError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Missing required field: {str(e)}'
            }, status=400)
        except Exception as e:
            logger.error(f'Error creating user: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to create user'
            }, status=500)


@method_decorator(handle_errors, name='dispatch')
class UserDetailView(View):
    """User detail view with caching"""
    
    def get(self, request, user_id):
        try:
            # Use cached method from model
            user = User.get_cached_user(user_id)
            
            if not user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'User not found'
                }, status=404)
            
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'is_active': user.is_active,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat()
                }
            })
            
        except Exception as e:
            logger.error(f'Error in UserDetailView: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to retrieve user'
            }, status=500)


@require_http_methods(["GET"])
@cache_page(60 * 10)  # Cache for 10 minutes
def posts_list(request):
    """Posts list view with optimized queries and caching"""
    try:
        posts = Post.get_published_posts_optimized()
        
        posts_data = [{
            'id': post.id,
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'author': post.author.username,
            'created_at': post.created_at.isoformat()
        } for post in posts]
        
        logger.info(f'Posts list retrieved - Count: {len(posts_data)}')
        
        return JsonResponse({
            'status': 'success',
            'data': posts_data,
            'count': len(posts_data)
        })
        
    except Exception as e:
        logger.error(f'Error in posts_list: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve posts'
        }, status=500)


def clear_cache_view(request):
    """Clear cache endpoint (for development/admin use)"""
    try:
        cache.clear()
        logger.info('Cache cleared successfully')
        return JsonResponse({
            'status': 'success',
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        logger.error(f'Error clearing cache: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to clear cache'
        }, status=500)
