from rest_framework import serializers
from .models import Transaction
from datetime import date

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'date', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future")
        return value

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'description']