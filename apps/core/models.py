from django.db import models
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger('myproject')


class Post(models.Model):
    """Post model with optimized queries"""
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    # Use the AUTH_USER_MODEL for author instead of a duplicate User
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
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
            posts = list(
                cls.objects.select_related('author')
                .filter(is_published=True)
                .only('title', 'content', 'created_at', 'author__username')
            )
            cache.set(cache_key, posts, timeout=600)  # Cache for 10 minutes
            logger.info('Published posts loaded from database and cached')
        else:
            logger.info('Published posts loaded from cache')

        return posts
