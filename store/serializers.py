from rest_framework import serializers
from .models import Category, Goods, Comment, PriceHistory
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'goods', 'rating', 'created', 'updated']

    def create(self, validated_data):
        author_id = self.context['request'].user.id
        author = get_user_model().objects.get(id=author_id)
        comment = Comment.objects.create(author=author, **validated_data)
        return comment
    
    def update(self, instance, validated_data):
        validated_data.pop('goods', None)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        '''
        т.к используем данный сериализатор для чтения в том числе, то удаляем goods
        т.к данный сериализатор будет вложенным в сериализатор для объекта Goods
        '''
        ret = super().to_representation(instance)
        ret.pop('goods')
        return ret
    

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'


class GoodsListSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = ['id', 'image', 'title', 'price', 'rating', 'available']

    def get_available(self, obj):
        if obj.amount >= 1:
            return True
        return False


class GoodsDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        exclude = ['slug']