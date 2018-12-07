from django import forms
from .models import UsuarioEmpresa, ImagenEmpleado


class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEmpresa
        fields = ('usuario', 'empresa')


class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('empleado', 'imagen')