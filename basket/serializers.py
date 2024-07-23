from rest_framework import serializers
from store.models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'title']


class BasketAddSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    override = serializers.BooleanField(required=False, default=False)


class BasketItemSerializer(serializers.Serializer):
    goods = GoodsSerializer()
    amount = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)