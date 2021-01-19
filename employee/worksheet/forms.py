from django import forms
from .models import UsuarioEmpresa, ImagenEmpleado, DeduccionesUnicasArchivo, DeduccionesEmpleadoArchivo

class UsuarioEmpresaForm(forms.ModelForm):
    class Meta:
        model = UsuarioEmpresa
        fields = ('usuario', 'empresa')

class ImagenEmpleadoForm(forms.ModelForm):
    class Meta:
        model = ImagenEmpleado
        fields = ('empleado', 'imagen')

class DeduccionArchivoForm(forms.Form):
    class Meta:
        model = DeduccionesUnicasArchivo
        fields = '__all__'

class DeduccionEmpleadoForm(forms.Form):
    class Meta:
        model = DeduccionesEmpleadoArchivo