# -*- encoding: utf-8 -*-
"""
Core views for GVRC Admin project
"""

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
import logging

# ✅ Use your custom user model
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()
logger = logging.getLogger(__name__)

# ----------------------------
# Health Check
# ----------------------------
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "service": "GVRC Admin",
        "timestamp": "2025-08-28"
    })


# ----------------------------
# Clear Cache
# ----------------------------
@require_http_methods(["GET"])
def clear_cache_view(request):
    """Clear cache endpoint (for dev/admin use)"""
    try:
        cache.clear()
        logger.info('Cache cleared successfully')
        return JsonResponse({
            "status": "success",
            "message": "Cache cleared successfully"
        })
    except Exception as e:
        logger.error(f'Error clearing cache: {str(e)}')
        return JsonResponse({
            "status": "error",
            "message": "Failed to clear cache"
        }, status=500)


# ----------------------------
# Posts List
# ----------------------------
@require_http_methods(["GET"])
@cache_page(60 * 10)  # Cache for 10 minutes
def posts_list(request):
    """Posts list view with pagination"""
    try:
        posts = Post.objects.all()  # 👈 remove filters first for debugging

        page = int(request.GET.get('page', 1))
        per_page = min(int(request.GET.get('per_page', 10)), 100)
        paginator = Paginator(posts, per_page)
        page_obj = paginator.get_page(page)

        posts_data = []
        for post in page_obj:
            try:
                posts_data.append({
                    "id": post.id,
                    "title": getattr(post, "title", ""),
                    "content": getattr(post, "content", "")[:200],
                    "author": getattr(post.author, "email", None) if hasattr(post, "author") else None,
                    "created_at": getattr(post, "created_at", None).isoformat() if getattr(post, "created_at", None) else None
                })
            except Exception as inner_e:
                logger.error(f"Error serializing post {post.id}: {inner_e}")

        return JsonResponse({
            "status": "success",
            "data": posts_data,
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_count": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        })

    except Exception as e:
        import traceback
        logger.error(f'Error retrieving posts: {str(e)}\n{traceback.format_exc()}')
        return JsonResponse({
            "status": "error",
            "message": f"Failed to retrieve posts: {str(e)}"
        }, status=500)

# ----------------------------
# User List (example)
# ----------------------------
@method_decorator(cache_page(60 * 5), name='dispatch')
class UserListView(View):
    """User list view"""
    def get(self, request):
        try:
            users = User.objects.filter(is_active=True).only(
                'id', 'username', 'email', 'first_name', 'last_name', 'date_joined'
            )
            data = [{
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "full_name": f"{u.first_name} {u.last_name}".strip(),
                "created_at": u.date_joined.isoformat()
            } for u in users]
            return JsonResponse({"status": "success", "data": data})
        except Exception as e:
            logger.error(f'Error retrieving users: {str(e)}')
            return JsonResponse({"status": "error", "message": "Failed to retrieve users"}, status=500)
