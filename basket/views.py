from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from store.models import Goods
from .shopping_basket import Basket
from .serializers import BasketAddSerializer, BasketItemSerializer


class BasketAddGoodsView(APIView):
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        data = request.data.copy() # request.data - неизменяемый QueryDict, а нужно pop()
        goods_id = data.pop('goods_id')
        goods = get_object_or_404(Goods, id=goods_id)
        serializer = BasketAddSerializer(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            basket.add(goods=goods, amount=data['amount'],
                       override_amount=data['override'])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BasketRemoveGoodsView(APIView):
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        goods = get_object_or_404(Goods, id=request.data['goods_id'])
        basket.remove(goods)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BasketDetailView(APIView):
    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        basket_items = basket.get_basket_items()
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)