from django.forms import ModelForm
from .models import Condominio

class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['codigo','nombre']