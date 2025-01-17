from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Goods, Comment, PriceHistory
from django.contrib.auth import get_user_model
from django.urls import reverse
from . import serializers
from orders.models import Order, OrderItem


def create_category(title):
    return Category.objects.create(title=title)


class StoreTest(APITestCase):
    def user_create(self, email='testuseremail@test.com', name='Test User',
                    password='89h2fffnw', auth_required=True):
        
        user = get_user_model().objects.create_user(email=email, name=name, password=password)
        is_authenticated = self.client.login(email=email, password=password)
        self.assertTrue(is_authenticated)
        return user

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

        self.order = Order.objects.create(user=self.user, status='succeeded')
        self.order_item = OrderItem.objects.create(order=self.order, goods=self.goods,
                                                   price=self.goods.price, amount=self.goods.amount)

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

    def test_goods_price_history(self):
        self.setup(auth_required=False)
        self.assertEqual(len(PriceHistory.objects.all()), 4)
        self.goods.price = 100
        self.goods.save()
        query = PriceHistory.objects.filter(goods=self.goods)
        self.assertEqual(len(query), 2)
        self.assertEqual(query[0].price, self.goods.price)
        self.assertEqual(len(serializers.GoodsDetailSerializer(self.goods).data['price_history']), 2)

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
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 5)

    def test_comment_partial_update(self):
        self.setup()
        comment = Comment.objects.create(author=self.user, body='Comment body',
                                         goods=self.goods, rating=5)
        url = reverse('store:comment_edit', args=[comment.id])
        data = {
            'body': 'Some other comment body',
            'rating': 3
        }
        full_data = {'goods': self.goods4.id, **data}

        response = self.client.patch(url, full_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 3)

        for key in data:
            self.assertEqual(getattr(comment, key), data[key])
        self.assertNotEqual(comment.goods.id, full_data['goods'])
        self.assertEqual(comment.goods.id, self.goods.id)

    def test_comment_partial_update_forbidden(self):
        self.setup(auth_required=False)
        user = self.user_create()
        comment = Comment.objects.create(author=self.user, body='Comment body',
                                         goods=self.goods, rating=5)
        url = reverse('store:comment_edit', args=[comment.id])
        data = {
            'body': 'Some other comment body',
            'rating': 5
        }
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertNotEqual(comment.body, data['body'])

    def test_comment_delete(self):
        self.setup()
        comment = Comment.objects.create(author=self.user, body='Comment body',
                                         goods=self.goods, rating=5)
        url = reverse('store:comment_edit', args=[comment.id])
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerySetEqual(Comment.objects.all(), [])
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 0)