# Generated by Django 5.0.7 on 2024-07-21 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_goods_comment_goods_store_goods_title_57e43a_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='count',
            new_name='amount',
        ),
    ]