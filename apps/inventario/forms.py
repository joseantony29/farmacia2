from django import forms
from .models import Laboratorio, TipoInsumo, Almacen, Producto

class FormLab(forms.ModelForm):
	class Meta:
		model = Laboratorio
		fields = '__all__'

class FormTipoInsu(forms.ModelForm):
	class Meta:
		model = TipoInsumo
		fields = '__all__'
		
class FormAlmacen(forms.ModelForm):
	class Meta:
		model = Almacen
		fields = '__all__'

class FormProducto(forms.ModelForm):
	class Meta:
		model = Producto
		fields = '__all__'