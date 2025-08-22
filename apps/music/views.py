# -*- encoding: utf-8 -*-
"""
Music views for GVRC Admin
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import Music, MusicPlay
from .forms import MusicForm
from apps.authentication.views import custom_login_required
import json
from django.contrib.auth import get_user_model
User = get_user_model()


@custom_login_required
def music_list(request):
    """Music list page with search and filtering"""
    # Get search parameters
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')
    artist = request.GET.get('artist', '')
    
    # Base queryset
    music_list = Music.objects.filter(is_active=True).select_related('created_by')
    
    # Apply filters
    if search:
        music_list = music_list.filter(
            Q(name__icontains=search) |
            Q(artist__icontains=search) |
            Q(description__icontains=search) |
            Q(genre__icontains=search)
        )
    
    if genre:
        music_list = music_list.filter(genre=genre)
    
    if artist:
        music_list = music_list.filter(artist=artist)
    
    # Get statistics
    total_tracks = music_list.count()
    total_listens = sum(track.total_listens for track in music_list)
    
    # Get unique genres and artists for filtering
    genres = Music.objects.filter(is_active=True).values_list('genre', flat=True).distinct().exclude(genre='').order_by('genre')
    artists = Music.objects.filter(is_active=True).values_list('artist', flat=True).distinct().exclude(artist='').order_by('artist')
    
    # Pagination
    paginator = Paginator(music_list.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'segment': 'music',
        'page_title': 'Music Library',
        'page_obj': page_obj,
        'music_list': music_list,
        'genres': genres,
        'artists': artists,
        'search': search,
        'selected_genre': genre,
        'selected_artist': artist,
        'total_tracks': total_tracks,
        'total_listens': total_listens,
    }
    
    return render(request, 'music/music_list.html', context)


@custom_login_required
def music_detail(request, music_id):
    """Music detail page"""
    music = get_object_or_404(Music, music_id=music_id, is_active=True)
    
    # Get recent plays for this track
    recent_plays = MusicPlay.objects.filter(music=music).select_related('user').order_by('-played_at')[:10]
    
    context = {
        'segment': 'music',
        'page_title': f'Music - {music.name}',
        'music': music,
        'recent_plays': recent_plays,
    }
    
    return render(request, 'music/music_detail.html', context)


@custom_login_required
def add_music(request):
    """Add new music track"""
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.created_by = request.user
            music.save()
            
            messages.success(request, f'Music track "{music.name}" added successfully!')
            return redirect('music:music_detail', music_id=music.music_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MusicForm()
    
    context = {
        'segment': 'music',
        'page_title': 'Add Music Track',
        'form': form,
    }
    
    return render(request, 'music/music_form.html', context)


@custom_login_required
def edit_music(request, music_id):
    """Edit existing music track"""
    music = get_object_or_404(Music, music_id=music_id, is_active=True)
    
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES, instance=music)
        if form.is_valid():
            music = form.save(commit=False)
            music.updated_by = request.user
            music.save()
            
            messages.success(request, f'Music track "{music.name}" updated successfully!')
            return redirect('music:music_detail', music_id=music.music_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MusicForm(instance=music)
    
    context = {
        'segment': 'music',
        'page_title': f'Edit Music - {music.name}',
        'form': form,
        'music': music,
    }
    
    return render(request, 'music/music_form.html', context)


@csrf_exempt
@require_POST
def track_play(request):
    """Track music play for analytics"""
    try:
        data = json.loads(request.body)
        music_id = data.get('music_id')
        user_id = data.get('user_id')
        session_duration = data.get('session_duration')
        
        if music_id and user_id:
            music = get_object_or_404(Music, music_id=music_id)
            user = get_object_or_404(User, id=user_id)
            
            MusicPlay.objects.create(
                music=music,
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                session_duration=session_duration
            )
            
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@custom_login_required
def music_analytics(request):
    """Music analytics dashboard"""
    # Get top tracks by listens
    top_tracks = Music.objects.filter(is_active=True).annotate(
        play_count=Count('musicplay')
    ).order_by('-play_count')[:10]
    
    # Get recent plays
    recent_plays = MusicPlay.objects.select_related('music', 'user').order_by('-played_at')[:20]
    
    # Get genre statistics
    genre_stats = Music.objects.filter(is_active=True).values('genre').annotate(
        track_count=Count('music_id'),
        total_plays=Count('musicplay')
    ).exclude(genre='').order_by('-total_plays')
    
    context = {
        'segment': 'music',
        'page_title': 'Music Analytics',
        'top_tracks': top_tracks,
        'recent_plays': recent_plays,
        'genre_stats': genre_stats,
    }
    
    return render(request, 'music/music_analytics.html', context)
