from django.db.models.signals import post_save, pre_delete
from django.db.models import Avg
from django.dispatch import receiver
from .models import PriceHistory, Goods, Comment

@receiver(post_save, sender=Goods)
def add_price_history(sender, instance, created, **kwargs):
    if created:
        PriceHistory.objects.create(goods=instance, price=instance.price)
    else:
        '''
        если цена в последнем по дате объекте PriceHistory не совпадает с текущей ценой товара -->
        цена товара изменилась и следует создать новый объект PriceHistory
        '''
        previous_price = PriceHistory.objects.filter(goods=instance).order_by('-date').first().price
        if previous_price != instance.price:
            PriceHistory.objects.create(goods=instance, price=instance.price)


@receiver(post_save, sender=Comment)
def update_goods_rating_if_save(sender, instance, **kwargs):
    goods = instance.goods
    comments = goods.comments.all()
    if comments.exists():
        goods.rating = comments.aggregate(Avg('rating'))['rating__avg']
    else:
        goods.raing = 0
    goods.save()

@receiver(pre_delete, sender=Comment)
def update_goods_rating_if_delete(sender, instance, **kwargs):
    goods = instance.goods
    comments = goods.comments.exclude(id=instance.id)
    if comments.exists():
        goods.rating = comments.aggregate(Avg('rating'))['rating__avg']
    else:
        goods.rating = 0
    goods.save()