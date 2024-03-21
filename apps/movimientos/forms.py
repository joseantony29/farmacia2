from django import forms
from .models import Ingreso, Solicitud, TipoMov
from apps.entidades.models import Beneficiado, User, Zona, Perfil

class IngresoForm(forms.ModelForm):
	tipo_ingreso = forms.ModelChoiceField(queryset=TipoMov.objects.filter(operacion=TipoMov.Operacion.SUMA))	
	class Meta:
		model = Ingreso
		fields = '__all__'

class MiSolicitudForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(MiSolicitudForm, self).__init__(*args, **kwargs)
		if user is not None:
			self.fields['beneficiado'].queryset = Beneficiado.objects.filter(perfil__cedula=user.perfil.cedula)

	class Meta:
		model = Solicitud
		fields = ['descripcion', 'recipe', 'beneficiado']

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud
		fields = '__all__'
		exclude = ['perfil']

class SolicitudPresencialForm(forms.ModelForm):
	class Meta:
		model = Solicitud
		fields = '__all__'
		
class PerfilForm(forms.ModelForm):
	nacionalidad = forms.ChoiceField(choices=Perfil.Nacionalidad.choices, initial=Perfil.Nacionalidad.VENEZOLANO)
	cedula = forms.CharField(max_length=8)
	nombres = forms.CharField(max_length=50)
	apellidos = forms.CharField(max_length=50)
	telefono = forms.CharField(max_length=11)
	genero = forms.ChoiceField(choices=Perfil.Genero.choices)
	f_nacimiento = forms.DateField()
	embarazada = forms.BooleanField()
	c_residencia = forms.FileField(required=False)
	zona = forms.ModelChoiceField(queryset=Zona.objects.all())
	direccion = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = User
		fields = '__all__'

class BeneficiadoForm(forms.ModelForm):
	class Meta:
		model = Beneficiado
		fields = '__all__'		

class SolicitudEditForm(forms.ModelForm):
	class Meta:
		model = Solicitud
		fields = '__all__'

class FormTipoMovi(forms.ModelForm):
	class Meta:
		model = TipoMov
		fields = '__all__'
