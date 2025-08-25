# -*- encoding: utf-8 -*-
"""
Template filters for chat app
"""

from django import template

register = template.Library()


@register.filter
def status_color(status):
    """Return Bootstrap color class for conversation status"""
    colors = {
        'new': 'info',
        'active': 'success',
        'resolved': 'secondary',
        'closed': 'danger'
    }
    return colors.get(status, 'secondary')


@register.filter
def priority_color(priority):
    """Return Bootstrap color class for conversation priority"""
    colors = {
        'urgent': 'danger',
        'high': 'warning',
        'medium': 'info',
        'low': 'success'
    }
    return colors.get(priority, 'info')
