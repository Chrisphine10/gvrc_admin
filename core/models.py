from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
import uuid

class TimestampedModel(models.Model):
    """Base model with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UserManager(models.Manager):
    """Custom manager for optimized queries"""
    
    def get_active_users(self):
        return self.select_related().filter(is_active=True)
    
    def get_users_with_posts(self):
        return self.prefetch_related('posts').filter(is_active=True)
    
    def search_users(self, query):
        return self.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(email__icontains=query)
        )

class User(AbstractUser):
    """Extended user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active', 'date_joined']),
            models.Index(fields=['last_activity']),
            models.Index(fields=['first_name', 'last_name']),
        ]
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def invalidate_cache(self):
        """Invalidate user-related cache"""
        cache_keys = [
            f"user_{self.id}",
            f"user_posts_{self.id}",
            "users_list*"
        ]
        for key in cache_keys:
            cache.delete_pattern(key)

class Category(TimestampedModel):
    """Post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name

class PostManager(models.Manager):
    """Custom manager for posts"""
    
    def published(self):
        return self.filter(status='published', published_at__isnull=False)
    
    def draft(self):
        return self.filter(status='draft')
    
    def by_category(self, category_slug):
        return self.filter(category__slug=category_slug)
    
    def recent(self, limit=10):
        return self.published().order_by('-published_at')[:limit]

class Post(TimestampedModel):
    """Blog posts"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    
    objects = PostManager()
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['slug']),
            models.Index(fields=['-published_at']),
        ]
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Increment view count efficiently"""
        Post.objects.filter(id=self.id).update(view_count=models.F('view_count') + 1)
        self.refresh_from_db(fields=['view_count'])

class Comment(TimestampedModel):
    """Post comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        indexes = [
            models.Index(fields=['post', 'is_approved']),
            models.Index(fields=['author']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.get_full_name()} on {self.post.title}"