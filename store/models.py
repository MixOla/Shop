from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Goods(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='goods')
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='goods/', blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    times_bought = models.PositiveIntegerField(default=0)
    # мб поле rating нужно на redis спихнуть т.к комментарии довольно динамичны --> и рейтинг тоже

    description = models.TextField()
    amount = models.PositiveIntegerField()

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category'])
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Goods, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class PriceHistory(models.Model): # Для истории цен, создание в signals.py
    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['goods']),
            models.Index(fields=['date'])
        ]

    def __str__(self):
        return f'{self.price} for {self.goods_id} on {self.date}'
    

class Comment(models.Model):
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='comments')
    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              related_name='comments')
    
    body = models.TextField(blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)