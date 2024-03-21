from datetime import date

from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User

from apps.entidades.models import Beneficiado, Perfil
from apps.inventario.models import Producto, Inventario

# solicitud de producto
class Solicitud(models.Model):
	
	class Status(models.TextChoices):
		EN_PROCRESO = 'PR', 'En Proceso'
		APROBADO = 'AP', 'Aprobado'
		EN_ESPERA_DE_ENTREGA = 'EE', 'En Espera de Entrega'
		ENTREGADO = 'ET', 'Entregado'
		RECHAZADO = 'RE', 'Rechazado'
	
	class TipoSoli(models.TextChoices):
		ONLINE = 'ON', 'En línea'
		PRESENCIAL = 'PR', 'Presencial'

	class FaseProceso(models.TextChoices):
		ADMINISTRADOR = 'AD', 'Administrador'
		ALMACENISTA = 'AL', 'Almacenista'
		AT_CLIENTE = 'AT', 'Atención al Cliente'

	fecha_soli = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
	perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, blank=False, null=False)
	beneficiado = models.ForeignKey(Beneficiado, on_delete=models.PROTECT, blank=False, null=False)
	descripcion = models.TextField(blank=False, null=False)
	recipe = models.ImageField(upload_to='recipes/', blank=False, null=False)
	proceso_actual = models.CharField(max_length=2, choices= FaseProceso.choices, default=FaseProceso.AT_CLIENTE)
	estado = models.CharField(max_length=2, choices=Status.choices, default=Status.EN_PROCRESO, blank=False, null=False)
	tipo_solicitud = models.CharField(choices=TipoSoli.choices, max_length=2)

	class Meta:
		verbose_name = 'Solicitud de Medicamento'
		verbose_name_plural = 'Solicitud de Medicamentos'
		ordering = ['fecha_soli']

	def __str__(self):
		return f'{self.descripcion}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

# detalle de la solicitud
class DetalleSolicitud(models.Model):
	solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalle')
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
	inventario = models.ManyToManyField(Inventario)
	cant_solicitada = models.IntegerField(default=1)
	cant_entregada = models.IntegerField(default=0)

	class Meta:
		unique_together = ('solicitud', 'producto')  # Asegurar que no haya duplicados
		verbose_name = 'Detalle de solicitud'
		verbose_name_plural = 'Detalle de solicitudes'
		ordering = ['pk']

	def __str__(self):
		return str(self.pk)

	def toJSON(self):
		item = model_to_dict(self)
		return item

# tipo de movimiento
class TipoMov(models.Model):

	class Operacion(models.TextChoices):
		SUMA = '+', 'Suma'
		RESTA = '-', 'Resta'

	nombre = models.CharField(max_length=50)
	operacion = models.CharField(choices=Operacion.choices, max_length=2)

	class Meta:
		verbose_name = 'Tipo de Movimiento'
		verbose_name_plural = 'Tipos de Movimientos'
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

class Jornada(models.Model):

	class Status(models.TextChoices):
		EN_PROCRESO = 'PR', 'En Proceso'
		APROBADO = 'AP', 'Aprobado'
		RECHAZADO = 'RE', 'Rechazado'

	class FaseProceso(models.TextChoices):
		ADMINISTRADOR = 'AD', 'Administrador'

	encargados = models.TextField()
	fecha = models.DateField(auto_now=False, auto_now_add=False)
	jefe_comunidad = models.ForeignKey(Perfil, on_delete=models.PROTECT)
	proceso_actual = models.CharField(max_length=2, choices= FaseProceso.choices, default=FaseProceso.ADMINISTRADOR)
	estado = models.CharField(max_length=2, choices=Status.choices, default=Status.EN_PROCRESO, blank=False, null=False)

	class Meta:
		verbose_name = 'Jornada'
		verbose_name_plural = 'Jornadas'
		ordering = ['pk']

	def __str__(self):
		return self.pk
	
	def toJSON(self):
		item = model_to_dict(self)
		return item

class DetalleJornada(models.Model):
	beneficiado = models.ForeignKey(Beneficiado, on_delete=models.PROTECT)
	productos = models.ManyToManyField(Producto)
	cant_solicitada = models.IntegerField()
	cant_aprobada = models.IntegerField()

	class Meta:
		verbose_name = 'Detalle de Jornada'
		verbose_name_plural = 'Detalle de Jornadas'
		ordering = ['pk']

	def __str__(self):
		return self.pk
	
	def toJSON(self):
		item = model_to_dict(self)
		return item

# movimiento del inventario
class Historial(models.Model):
	fecha_mov = models.DateField(auto_now_add=True, blank=False, null=False)
	tipo_mov = models.ForeignKey(TipoMov, on_delete=models.PROTECT)
	empleado = models.ForeignKey(Perfil, on_delete=models.PROTECT)
	producto = models.ForeignKey(Inventario, on_delete=models.PROTECT, related_name='historial')
	cantidad = models.IntegerField(blank=False, null=False)

	def crear_movimiento(self, datos):
		movimiento = Historial()
		movimiento.tipo_mov = datos['tipo_mov']
		movimiento.empleado = datos['perfil']
		movimiento.producto = datos['producto']
		movimiento.cantidad = datos['cantidad']
		movimiento.save()

	class Meta:
		verbose_name = 'Movimiento de Inventario'
		verbose_name_plural = 'Movimientos de Inventario'
		ordering = ['-pk']

	def __str__(self):
		return str(self.pk)
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
class Ingreso(models.Model):
	fecha = models.DateField(auto_now=False, auto_now_add=False)
	descripcion= models.TextField()
	tipo_ingreso = models.ForeignKey(TipoMov, on_delete=models.PROTECT)

	class Meta:
		verbose_name = 'Ingreso'
		verbose_name_plural = 'Ingresos'
		ordering = ['pk']

	def __str__(self):
		return str(self.pk)
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
class DetalleIngreso(models.Model):
	ingreso = models.ForeignKey(Ingreso, on_delete=models.PROTECT, related_name='detalle')
	inventario = models.ForeignKey(Inventario, on_delete=models.PROTECT)
	cantidad = models.IntegerField()
	lote = models.CharField(max_length=50)
	f_vencimiento = models.DateField(auto_now=False, auto_now_add=False)

	class Meta:
		verbose_name = 'Detalle de ingreso'
		verbose_name_plural = 'Detalles de ingresos'

	def __str__(self):
		return str(self.pk)
	
	def toJSON(self):
		item = model_to_dict(self)
		return item