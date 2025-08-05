# -*- encoding: utf-8 -*-
"""
Home app views
"""

from django.shortcuts import render

def home_view(request):
    """Home page view"""
    return render(request, 'pages/index.html')

# Keep backward compatibility
index = home_view
