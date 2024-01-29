from rest_framework import serializers
from .models import StockStalk


class StockStalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockStalk
        fields = "__all__"
