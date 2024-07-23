from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Goods, Comment
from django.contrib.auth import get_user_model
from django.urls import reverse
from . import serializers


def create_category(title):
    return Category.objects.create(title=title)


class StoreTest(APITestCase):
    def setup(self, auth_required=True):
        self.category = Category.objects.create(title='First Category')
        self.category2 = Category.objects.create(title='Second Category')
        self.category3 = Category.objects.create(title='Third Category')
        self.goods = Goods.objects.create(title='First Goods', price='6',
                                          amount=1, category=self.category,
                                          times_bought=2)
        self.goods2 = Goods.objects.create(title='Second Goods', price='25',
                                           amount=1, category=self.category,
                                           times_bought=3)
        self.goods3 = Goods.objects.create(title='Third Goods', price='2',
                                           amount=1, category=self.category2,
                                           times_bought=8)
        self.goods4 = Goods.objects.create(title='Fourth Goods', price='10',
                                           amount=1,category=self.category3,
                                           times_bought=6)
        self.email = 'test@test.com'
        self.password = 'password123'
        self.user = get_user_model().objects.create_user(
            email=self.email,
            name='Name',
            password=self.password,
            categories_bought={self.category.title: 3, self.category2.title: 1}
        )
        if auth_required:
            is_authenticated = self.client.login(email=self.email,
                                                 password=self.password)
            self.assertTrue(is_authenticated)

    def test_goods_list_no_filter(self):
        self.setup()
        url = reverse('store:goods_list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0], serializers.GoodsListSerializer(self.goods2).data)
        self.assertEqual(data[1], serializers.GoodsListSerializer(self.goods).data)
        self.assertEqual(data[2], serializers.GoodsListSerializer(self.goods3).data)
        self.assertEqual(data[3], serializers.GoodsListSerializer(self.goods4).data)

    def test_goods_list_category_filter(self):
        self.setup()
        url = reverse('store:goods_category_list', args=(self.category.title, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], serializers.GoodsListSerializer(self.goods2).data)
        self.assertEqual(data[1], serializers.GoodsListSerializer(self.goods).data)

    def test_goods_list_title_filter(self):
        self.setup()
        url = reverse('store:goods_list')

        response = self.client.get(url, {'title': 'd Goods'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data[0], serializers.GoodsListSerializer(self.goods2).data)
        self.assertEqual(data[1], serializers.GoodsListSerializer(self.goods3).data)
    
    def test_goods_price_filter(self):
        self.setup()
        url = reverse('store:goods_list')
        
        response = self.client.get(url, {'price': '5;25'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data[0], serializers.GoodsListSerializer(self.goods2).data)
        self.assertEqual(data[1], serializers.GoodsListSerializer(self.goods).data)
        self.assertEqual(data[3], serializers.GoodsListSerializer(self.goods4).data)

    def test_goods_detail(self):
        self.setup()
        url = reverse('store:goods_detail', args=(self.goods.id, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializers.GoodsDetailSerializer(self.goods).data)

    def test_comment_create(self):
        self.setup()
        url = reverse('store:comment_create', args=[self.goods.id])
        data = {
            'body': 'Some comment body',
            'rating': 5,
            'goods': self.goods.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)