from django.db import models

# Create your models here.
class Restaurante(models.Model):
    name = models.TextField(verbose_name='Nombre')
    food = models.TextField(verbose_name='Tipos de Comida', default='Otro')
    points = models.FloatField(verbose_name='Puntuacion',default=0.0)
    num_reviews = models.IntegerField(verbose_name='Numero de puntuaciones',default=0) 
    min_price = models.IntegerField(verbose_name='Menor precio',default=0)
    max_price = models.IntegerField(verbose_name='Mayor precio',default=0)
    location = models.TextField(verbose_name="Ubicacion", default="Desconocido")