# Generated by Django 5.0.7 on 2024-07-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('slug', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['title'],
                'indexes': [models.Index(fields=['title'], name='store_categ_title_e79325_idx')],
            },
        ),
    ]
