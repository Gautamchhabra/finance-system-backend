from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'type', 'category', 'date']
    list_filter = ['type', 'category', 'date', 'user']
    search_fields = ['description', 'category']
    date_hierarchy = 'date'