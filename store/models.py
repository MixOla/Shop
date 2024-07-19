from django.db import models
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


class Good(models.Model):
    pass