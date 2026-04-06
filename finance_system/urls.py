from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transactions.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Login/logout views
]