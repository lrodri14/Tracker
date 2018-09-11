from django import forms
from .models import UsuarioEmpresa


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEmpresa
        fields = ('usuario', 'empresa')
