from django.db import models
from django.core.cache import cache
import logging

logger = logging.getLogger('myproject')

class User(models.Model):
    """User model with caching and optimization"""
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.username

    @classmethod
    def get_cached_user(cls, user_id):
        """Get user with caching"""
        cache_key = f'user:{user_id}'
        user = cache.get(cache_key)
        
        if user is None:
            try:
                user = cls.objects.select_related().get(id=user_id)
                cache.set(cache_key, user, timeout=300)  # Cache for 5 minutes
                logger.info(f'User {user_id} loaded from database and cached')
            except cls.DoesNotExist:
                logger.warning(f'User {user_id} not found')
                return None
        else:
            logger.info(f'User {user_id} loaded from cache')
        
        return user

    def invalidate_cache(self):
        """Invalidate user cache when updated"""
        cache_key = f'user:{self.id}'
        cache.delete(cache_key)
        logger.info(f'Cache invalidated for user {self.id}')

    def save(self, *args, **kwargs):
        """Override save to invalidate cache"""
        super().save(*args, **kwargs)
        self.invalidate_cache()


class Post(models.Model):
    """Post model with optimized queries"""
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'posts'
        indexes = [
            models.Index(fields=['is_published', 'created_at']),
            models.Index(fields=['author', 'is_published']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @classmethod
    def get_published_posts_optimized(cls):
        """Get published posts with optimized query"""
        cache_key = 'published_posts'
        posts = cache.get(cache_key)
        
        if posts is None:
            posts = list(cls.objects.select_related('author')
                        .filter(is_published=True)
                        .only('title', 'content', 'created_at', 'author__username'))
            cache.set(cache_key, posts, timeout=600)  # Cache for 10 minutes
            logger.info('Published posts loaded from database and cached')
        else:
            logger.info('Published posts loaded from cache')
        
        return posts
