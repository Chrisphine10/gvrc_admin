import time
from django.db.models import Count, Q, Prefetch
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Post, Category, Comment
from ..serializers import (UserSerializer, PostListSerializer, 
                          PostDetailSerializer, CategorySerializer)
from ..services.cache_service import CacheService

User = get_user_model()

@api_view(['GET'])
def user_list(request):
    """
    Optimized user list with search, pagination, and caching
    """
    start_time = time.time()
    
    # Get query parameters
    search = request.GET.get('search', '').strip()
    page = int(request.GET.get('page', 1))
    per_page = min(int(request.GET.get('per_page', 15)), 100)  # Max 100 per page
    
    # Generate cache key
    cache_key = CacheService.generate_key('query',
        type='users',
        search=search,
        page=page,
        per_page=per_page
    )
    
    def fetch_users():
        # Build optimized query
        queryset = User.objects.select_related().annotate(
            posts_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(is_active=True)
        
        # Apply search filter
        if search:
            queryset = User.objects.search_users(search)
        
        # Order by activity
        queryset = queryset.order_by('-last_activity', '-date_joined')
        
        # Paginate
        paginator = Paginator(queryset, per_page)
        users_page = paginator.get_page(page)
        
        # Serialize
        serializer = UserSerializer(users_page, many=True)
        
        return {
            'users': serializer.data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'has_next': users_page.has_next(),
                'has_previous': users_page.has_previous()
            }
        }
    
    # Get from cache or execute query
    result = CacheService.get_or_set(cache_key, fetch_users, CacheService.SHORT_TTL)
    
    return Response({
        'status': 'success',
        'data': result,
        'meta': {
            'response_time': round((time.time() - start_time) * 1000, 2),
            'cached': True if CacheService.get(cache_key) else False
        }
    })

@api_view(['GET'])
def user_detail(request, user_id):
    """Get user details with posts"""
    cache_key = CacheService.generate_key('user', user_id=user_id, detail=True)
    
    def fetch_user():
        try:
            user = User.objects.select_related().prefetch_related(
                Prefetch('posts', 
                        queryset=Post.objects.filter(status='published')
                                           .order_by('-published_at')[:10])
            ).get(id=user_id, is_active=True)
            
            serializer = UserSerializer(user)
            recent_posts = PostListSerializer(user.posts.all()[:10], many=True)
            
            return {
                'user': serializer.data,
                'recent_posts': recent_posts.data
            }
        except User.DoesNotExist:
            return None
    
    result = CacheService.get_or_set(cache_key, fetch_user, CacheService.DEFAULT_TTL)
    
    if result is None:
        return Response({
            'status': 'error',
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    