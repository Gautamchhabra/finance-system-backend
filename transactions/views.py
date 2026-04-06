from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateSerializer
from users.permissions import RoleBasedPermission
from datetime import datetime

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'date']
    search_fields = ['description', 'category']
    ordering_fields = ['amount', 'date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        """Users can only see their own transactions"""
        return Transaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a transaction"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def filter_by_date_range(self, request):
        """Custom endpoint to filter by date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = self.get_queryset()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get transactions grouped by category"""
        queryset = self.get_queryset()
        categories = queryset.values('category').annotate(
            total=models.Sum('amount'),
            count=models.Count('id')
        )
        return Response(categories)