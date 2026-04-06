from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractYear, ExtractMonth
from transactions.models import Transaction
from users.models import UserRole
from datetime import datetime, timedelta
from calendar import month_name

class FinancialSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Check if user has permission to view analytics
        if user.role == UserRole.VIEWER:
            # Viewers can view analytics
            pass
        elif user.role in [UserRole.ANALYST, UserRole.ADMIN]:
            pass
        else:
            return Response({"error": "Permission denied"}, status=403)
        
        transactions = Transaction.objects.filter(user=user)
        
        # Calculate totals
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expenses
        
        # Category breakdown
        category_breakdown = transactions.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Monthly totals (last 6 months)
        today = datetime.now().date()
        six_months_ago = today - timedelta(days=180)
        
        monthly_totals = transactions.filter(date__gte=six_months_ago).values(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        ).annotate(
            income=Sum('amount', filter=Q(type='income')),
            expense=Sum('amount', filter=Q(type='expense'))
        ).order_by('-year', '-month')
        
        # Format monthly data
        monthly_data = []
        for item in monthly_totals:
            monthly_data.append({
                'month': f"{month_name[item['month']]} {item['year']}",
                'income': float(item['income'] or 0),
                'expense': float(item['expense'] or 0),
                'balance': float((item['income'] or 0) - (item['expense'] or 0))
            })
        
        # Recent activity (last 10 transactions)
        recent = transactions[:10]
        recent_data = [{
            'date': t.date,
            'type': t.type,
            'category': t.category,
            'amount': float(t.amount),
            'description': t.description
        } for t in recent]
        
        return Response({
            'summary': {
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'balance': float(balance),
                'total_transactions': transactions.count()
            },
            'category_breakdown': [
                {
                    'category': item['category'],
                    'total': float(item['total']),
                    'count': item['count']
                } for item in category_breakdown
            ],
            'monthly_totals': monthly_data,
            'recent_activity': recent_data
        })

class CategoryAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, category=None):
        user = request.user
        
        # Check permission
        if user.role == UserRole.VIEWER:
            # Viewers can view analytics
            pass
        elif user.role in [UserRole.ANALYST, UserRole.ADMIN]:
            pass
        else:
            return Response({"error": "Permission denied"}, status=403)
        
        transactions = Transaction.objects.filter(user=user)
        
        if category:
            transactions = transactions.filter(category=category)
        
        analytics = transactions.values('type').annotate(
            total=Sum('amount'),
            average=Sum('amount')/Count('id'),
            count=Count('id')
        )
        
        return Response({
            'category': category if category else 'All Categories',
            'analytics': [
                {
                    'type': item['type'],
                    'total': float(item['total'] or 0),
                    'average': float(item['average'] or 0),
                    'count': item['count']
                } for item in analytics
            ]
        })