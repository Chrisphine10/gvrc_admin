rom rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsFacilityOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a facility to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner or creator of the facility
        return obj.created_by == request.user or request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner of the object
        return obj.user == request.user or request.user.is_staff


class IsOwnerOrStaff(BasePermission):
    """
    Custom permission to only allow owners or staff to access object.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow access if user is staff
        if request.user.is_staff:
            return True
        
        # Allow access if user is the owner
        return obj.user == request.user


class IsFacilityManagerOrReadOnly(BasePermission):
    """
    Permission for facility managers to edit facility-related data
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is associated with the facility
        if hasattr(obj, 'facility'):
            return (obj.facility.created_by == request.user or 
                   request.user.facility == obj.facility or 
                   request.user.is_staff)
        
        return request.user.is_staff