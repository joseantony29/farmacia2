from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import (
	UpdateView,
	ListView,
	CreateView,
	DetailView,
	View, 
	TemplateView
)
from apps.entidades.mixins import ValidarUsuario
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FormLab, FormTipoInsu, FormAlmacen, FormProducto

from .models import Producto, Inventario, Laboratorio, TipoInsumo, Almacen
from apps.movimientos.models import Historial

# Create your views here.
	
class DetalleProductoView(ValidarUsuario, DetailView):
	permission_required = 'inventario.view_producto'
	template_name = 'pages/productos/detalle_producto.html'
	# permission_required = 'anuncios.requiere_secretria'
	model = Producto
	context_object_name = 'producto'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		producto = Producto.objects.filter(pk=self.kwargs.get('pk')).first()
		inventario = Inventario.objects.filter(producto_id=producto.pk, f_vencimiento__gt=date.today(), stock__gt=0).order_by('f_vencimiento')
		if inventario:
			context["inventario"] = inventario

		if producto:
			for i in Inventario.objects.filter(producto_id=producto.pk).order_by('f_vencimiento'):
				historial = Historial.objects.filter(producto__producto__id=i.producto.pk).order_by('-pk')
				if historial:
					context["historial"] = historial
			
		context["sub_title"] = "Detalles del producto"
		return context

class ListadoProductos(ValidarUsuario, TemplateView):
	permission_required = 'inventario.view_producto'
	template_name = 'pages/productos/listado_productos.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_productos':
				data = []
				for i in Producto.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de productos"
		context["form"] = FormProducto()
		return context
	
class RegistrarProducto(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_producto':
				form = FormProducto(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title': 'Exito!', 'data': 'Producto registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title': 'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class ActualizarProducto(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_producto':
				print(request.POST)
				producto = Producto.objects.filter(id = request.POST['id']).first()
				form = FormProducto(request.POST, instance=producto)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'El producto se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	

class ListadoLaboratorio(ValidarUsuario, TemplateView):
	permission_required = 'inventario.view_laboratorio'
	template_name = "pages/mantenimiento/listado_lab.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_labs':
				data = []
				for i in Laboratorio.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de Laboratorios"
		return context
	
class RegistrarLab(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			print(request.POST)

			if action == 'nuevo_lab':
				form = FormLab(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title': 'Exito!', 'data': 'Laboratorio registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title': 'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ActualizarLaboratorio(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_lab':
				laboratorio = Laboratorio.objects.filter(id = request.POST['id']).first()
				form = FormLab(request.POST, instance=laboratorio)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'El Laboratorio se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	
	
class ListadoTiposInsumos(ValidarUsuario, TemplateView):
	permission_required = 'inventario.view_tipoinsumo'
	template_name = "pages/mantenimiento/tipo_insu.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_tipo_ins':
				data = []
				for i in TipoInsumo.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de tipos de insumos"
		return context
	
class RegistrarTipoInsu(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_tipo_insu':
				form = FormTipoInsu(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Tipo de insumo registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class ActualizarTipoInsumo(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_t_ins':
				tipo_insu = TipoInsumo.objects.filter(id = request.POST['id']).first()
				form = FormLab(request.POST, instance=tipo_insu)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'El tipo de insumo se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	
	
class ListadoAlmacen(ValidarUsuario, TemplateView):
	permission_required = 'inventario.view_almacen'
	template_name = "pages/mantenimiento/listado_almacen.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_almacen':
				data = []
				for i in Almacen.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de almacenes"
		return context

class RegistrarAlmacen(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_almacen':
				form = FormAlmacen(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Almacen registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ActualizarAlmacen(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_almacen':
				almacen = Almacen.objects.filter(id = request.POST['id']).first()
				form = FormAlmacen(request.POST, instance=almacen)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'El Almacen se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	