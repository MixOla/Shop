# Generated by Django 5.0.7 on 2024-07-24 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_count_goods_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='store.goods')),
            ],
            options={
                'ordering': ['-date'],
                'indexes': [models.Index(fields=['goods'], name='store_price_goods_i_36b25a_idx'), models.Index(fields=['date'], name='store_price_date_48d979_idx')],
            },
        ),
    ]
