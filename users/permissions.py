from rest_framework import permissions
from .models import UserRole

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission to check user roles for different actions
    """
    
    def has_permission(self, request, view):
        # Allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can do everything
        if request.user.role == UserRole.ADMIN:
            return True
        
        # For ViewSet actions (transactions)
        if hasattr(view, 'action'):
            if view.action in ['list', 'retrieve']:
                # Viewers, analysts, and admins can view
                return True
            elif view.action in ['create', 'update', 'partial_update', 'destroy']:
                # Only admin and analyst can modify
                return request.user.role in [UserRole.ADMIN, UserRole.ANALYST]
        
        # For regular APIView classes (like analytics)
        # GET requests are view operations
        if request.method == 'GET':
            return True
        # POST, PUT, DELETE require higher privileges
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in [UserRole.ADMIN, UserRole.ANALYST]
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Users can only access their own transactions
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.role == UserRole.ADMIN
        return True