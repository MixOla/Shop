from rest_framework import serializers
from .models import Category, Goods, Comment
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Comment
        fields = ['author', 'body', 'goods', 'rating', 'created', 'updated']

    def create(self, validated_data):
        author_id = self.context['request'].user.id
        author = get_user_model().objects.get(id=author_id)
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class GoodsListSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = ['image', 'title', 'price', 'rating', 'available']

    def get_available(self, obj):
        if obj.amount >= 1:
            return True
        return False


class GoodsDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        exclude = ['slug']