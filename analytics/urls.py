from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.FinancialSummaryView.as_view(), name='summary'),
    path('category-analytics/', views.CategoryAnalyticsView.as_view(), name='category-analytics'),
    path('category-analytics/<str:category>/', views.CategoryAnalyticsView.as_view(), name='category-analytics-detail'),
]