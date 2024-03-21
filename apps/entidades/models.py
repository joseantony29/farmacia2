from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User

# zona
class Zona(models.Model):
	zona_residencia = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Zona'
		verbose_name_plural = 'Zonas'

	def __str__(self):
		return self.zona_residencia

	def toJSON(self):
		item = model_to_dict(self)
		return item

class Persona(models.Model):

	class Genero(models.TextChoices):
		MASCULINO = 'MA', 'Masculino'
		FEMENINO = 'FE', 'Femenino'

	class Nacionalidad(models.TextChoices):
		VENEZOLANO = 'V-', 'V-'
		EXTRANJERO = 'E-', 'E-'
		JURIDICO = 'J-', 'J-'
	
	class CodigoTlf(models.TextChoices):
		C412 = '0412', '0412'
		C414 = '0414', '0414'
		C416 = '0416', '0416'
		C424 = '0424', '0424'
		C426 = '0426', '0426'

	nacionalidad = models.CharField(max_length=2, choices=Nacionalidad.choices, default=Nacionalidad.VENEZOLANO, blank=False, null=False)
	cedula = models.CharField(max_length=8, blank=False, null=False)
	nombres = models.CharField(max_length=50, blank=False, null=False)
	apellidos = models.CharField(max_length=50, blank=False, null=False)
	telefono = models.CharField(max_length=11, blank=False, null=False)
	genero = models.CharField(max_length=2, blank=False, null=False, choices=Genero.choices)
	f_nacimiento = models.DateField(auto_now_add = False, auto_now=False, blank=False, null=False)
	embarazada = models.BooleanField(blank=False, null=False)
	c_residencia = models.FileField(upload_to='constancias_residencias/', blank=True, null=True)
	zona  = models.ForeignKey(Zona, on_delete=models.PROTECT, blank=False, null=False)
	direccion = models.TextField(blank=False, null=False)
	
	class Meta:
		abstract = True

	def toJSON(self):
		item = model_to_dict(self)
		if self.c_residencia:
			item['c_residencia'] = self.c_residencia.url
		else:
			item['c_residencia'] = None
		return item

class Perfil(Persona):
	class Rol(models.TextChoices):
		ADMINISTRADOR = 'AD', 'Administrador'
		ALMACENISTA = 'AL', 'Almacenista'
		AT_CLIENTE = 'AT', 'Atención al Cliente'
		JEFE_COMUNIDAD = 'JC', 'Jefe de Comunidad'
		PACIENTE = 'PA', 'Paciente'
	
	rol = models.CharField(max_length=2, choices=Rol.choices, default=Rol.PACIENTE)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
	
	def __str__(self):
		return f'{self.cedula}-{self.nombres}'
	
	class Meta:
		verbose_name = 'perfil'
		verbose_name_plural = 'perfiles'
		permissions = [
			('cambiar_password', 'cambiar contraseña a usuarios'),
			('cambiar_estado_usuarios', 'cambiar estado de usuarios'),
			('cambiar_estado_jornada', 'cambiar estatus de jornadas'),
			('cambiar_estado_solicitudes', 'cambiar status de solicitudes'),
			('entregar_solicitud_medicamentos', 'Entregar solicitud de medicamentos'),
			('entregar_jornada_medicamentos', 'Entregar jornada de medicamentos'),
			('ver_inicio', 'Ver inicio'),
			('ver_mis_solicitudes_de_medicamentos', 'Ver mis solicitudes de medicamentos'),
			('ver_mis_jornada_medicamentos', 'Ver mis jornadas de medicamentos'),
			('registrar_mi_solicitud_de_medicamentos', 'Registrar mi solicitud de medicamentos'),
			('registrar_mi_jornada_medicamentos', 'Registrar mi jornada de medicamentos')
		]

	def toJSON(self):
		item = model_to_dict(self)
		if self.c_residencia:
			item['c_residencia'] = self.c_residencia.url
		else:
			item['c_residencia'] = None
		item['usuario'] = {'id': self.usuario.pk, 'username': self.usuario.username, 'is_active': self.usuario.is_active}
		item['zona'] = {'id': self.zona.pk, 'zona_residencia': self.zona.zona_residencia}
		item['genero'] = self.get_genero_display()
		return item

class Beneficiado(Persona):
	perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, related_name='beneficiados')

	def __str__(self):
		return f'{self.cedula}-{self.nombres}'
		
	class Meta:
		verbose_name = 'Beneficiado'
		verbose_name_plural = 'Beneficiados'

	def toJSON(self):
		item = model_to_dict(self)
		if self.c_residencia:
			item['c_residencia'] = self.c_residencia.url
		else:
			item['c_residencia'] = None
		return item

# personalizar landing

class LandingPage(models.Model):
	imagen1 = models.ImageField(upload_to='images_landing/', blank=True, null=True)
	imagen2 = models.ImageField(upload_to='images_landing/', blank=True, null=True)
	imagen3 = models.ImageField(upload_to='images_landing/', blank=True, null=True)
	imagen4 = models.ImageField(upload_to='images_landing/', blank=True, null=True)
	imagen5 = models.ImageField(upload_to='images_landing/', blank=True, null=True)
	texto1 = models.TextField(blank=True, null=True)

	def __str__(self) -> str:
		return super().__str__()
	
	@classmethod
	def get_config(cls):
		conf, created = cls.objects.get_or_create()
		return conf
	
	class Meta:
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes'

	def toJSON(self):
		item = model_to_dict(self)
		return item