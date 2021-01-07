from django import forms
from .models import Restaurante

class BusquedaPorNombre(forms.Form):
    nombre = forms.CharField(label="Nombre del Restaurante")
