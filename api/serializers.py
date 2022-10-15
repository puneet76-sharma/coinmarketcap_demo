from rest_framework import serializers
from .models import CoinMarket

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinMarket
        fields='__all__'