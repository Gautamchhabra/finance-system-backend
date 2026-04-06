from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class UserRole(models.TextChoices):
    VIEWER = 'viewer', 'Viewer'
    ANALYST = 'analyst', 'Analyst'
    ADMIN = 'admin', 'Admin'

class User(AbstractUser):
    # Extend Django's built-in User model
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.VIEWER
    )
    
    def has_permission(self, action, model_name='transaction'):
        """Check if user has permission for specific action"""
        if self.role == UserRole.ADMIN:
            return True
        elif self.role == UserRole.ANALYST:
            return action in ['view', 'filter', 'analyze']
        elif self.role == UserRole.VIEWER:
            return action == 'view'
        return False
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"