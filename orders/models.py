from django.db import models
from django.contrib.auth import get_user_model
from store.models import Goods


class Order(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.DO_NOTHING,
                             related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Order {self.id}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,
                              related_name='order_items',
                              on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderItem {self.id}'
    
    def get_total_price(self):
        return self.price * self.amount