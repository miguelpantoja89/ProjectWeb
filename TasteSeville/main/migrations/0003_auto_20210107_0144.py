# Generated by Django 3.1.3 on 2021-01-07 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210107_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='location',
            field=models.TextField(default='Desconocido', verbose_name='Ubicacion'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='location_url',
            field=models.URLField(default='', verbose_name='URL Google Maps'),
        ),
    ]
