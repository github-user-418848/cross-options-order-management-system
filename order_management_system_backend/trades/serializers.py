from rest_framework import serializers
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        exclude = ['total_amount_paid']

class TradeWithTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        
class TradeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['amount_of_shares_bought', 'price_per_share']