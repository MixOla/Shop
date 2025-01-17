# Generated by Django 5.0.7 on 2024-07-21 21:16

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(blank=True, upload_to='goods/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('times_bought', models.PositiveIntegerField(default=0)),
                ('description', models.TextField()),
                ('count', models.PositiveIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goods', to='store.category')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='store.goods')),
            ],
        ),
        migrations.AddIndex(
            model_name='goods',
            index=models.Index(fields=['title'], name='store_goods_title_57e43a_idx'),
        ),
        migrations.AddIndex(
            model_name='goods',
            index=models.Index(fields=['category'], name='store_goods_categor_5b4944_idx'),
        ),
    ]
