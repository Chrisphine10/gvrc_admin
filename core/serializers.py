from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """User serializer with performance optimization"""
    full_name = serializers.ReadOnlyField()
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'full_name', 'bio', 'avatar', 'is_verified', 'posts_count']
        read_only_fields = ['id', 'is_verified']
    
    def get_posts_count(self, obj):
        # Use prefetch_related or annotate to avoid N+1 queries
        return getattr(obj, 'posts_count', obj.posts.count())

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']
    
    def get_posts_count(self, obj):
        return getattr(obj, 'posts_count', obj.posts.filter(status='published').count())

class PostListSerializer(serializers.ModelSerializer):
    """Optimized serializer for post lists"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author_name', 
                 'category_name', 'status', 'published_at', 'view_count', 'like_count']

class PostDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single post"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 
                 'category', 'status', 'published_at', 'view_count', 
                 'like_count', 'comments_count', 'created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        return getattr(obj, 'comments_count', obj.comments.filter(is_approved=True).count())

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'created_at', 'replies_count']
    
    def get_replies_count(self, obj):
        return obj.replies.filter(is_approved=True).count()