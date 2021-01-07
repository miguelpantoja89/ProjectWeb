# Generated by Django 3.1.3 on 2021-01-06 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='food',
            field=models.TextField(default='Otro', verbose_name='Tipos de Comida'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='max_price',
            field=models.IntegerField(default=0, verbose_name='Mayor precio'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='min_price',
            field=models.IntegerField(default=0, verbose_name='Menor precio'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='num_reviews',
            field=models.IntegerField(default=0, verbose_name='Numero de puntuaciones'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='points',
            field=models.FloatField(default=0.0, verbose_name='Puntuacion'),
        ),
    ]
