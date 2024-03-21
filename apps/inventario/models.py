from datetime import date
from django.db import models
from django.forms import model_to_dict

# ubicacion del producto
class Almacen(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Ubicación'
		verbose_name_plural = 'Ubicaciones'

	def __str__(self):
		return f'{self.nombre}'
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# tipo de insumo
class TipoInsumo(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Tipo de insumo'
		verbose_name_plural = 'Tipo de insumos'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# laboratorio
class Laboratorio(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Laboratorio'
		verbose_name_plural = 'Laboratorios'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# productos
class Producto(models.Model):

	class Seleccion(models.TextChoices):
		SI = 'SI', 'SÍ'
		NO = 'NO', 'NO'

	nombre = models.CharField(max_length=50, blank=False, null=False)
	almacen = models.ForeignKey(Almacen, verbose_name='Ubicación', on_delete=models.PROTECT, blank=False, null=False)
	tipo_insumo = models.ForeignKey(TipoInsumo, verbose_name='Tipo de insumo', on_delete=models.PROTECT, blank=False, null=False)
	laboratorio = models.ForeignKey(Laboratorio, verbose_name='Laboratorio', on_delete=models.PROTECT, blank=False, null=False)
	if_expire_date = models.CharField(verbose_name='Si caduca', max_length = 2, choices = Seleccion.choices)
	stock_minimo = models.IntegerField(blank=False, null=False)
	total_stock = models.IntegerField(null = False, blank= False)

	def contar_productos(self):
		self.total_stock = 0
		for i in self.inventario.filter(f_vencimiento__gt=date.today(), stock__gt=0):
			self.total_stock += i.stock
		self.save()

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre}'

	def toJSON(self):
		item = model_to_dict(self)
		item['almacen'] = {'nombre': self.almacen.nombre, 'id': self.almacen.pk}
		item['laboratorio'] = {'nombre':self.laboratorio.nombre, 'id': self.laboratorio.pk}
		item['tipo_insumo'] = {'nombre': self.tipo_insumo.nombre, 'id': self.tipo_insumo.pk}
		return item

class Inventario(models.Model):
	lote = models.CharField(max_length=50,verbose_name='Codigo de lote')
	f_vencimiento = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de vencimiento')
	stock = models.IntegerField(default=0, verbose_name='Stock')
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventario', verbose_name='Producto')

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventarios'
		# permissions = [
		# 	("can_view_student", "Can view student"),
		# ]

	def __str__(self):
		return "{} - {}".format(self.producto.nombre, self.lote)

	def toJSON(self):
		item = model_to_dict(self)
		return item
