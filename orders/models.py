from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.DO_NOTHING,
                             related_name='orders')