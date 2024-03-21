from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

from apps.movimientos.models import TipoMov
from apps.movimientos.forms import FormTipoMovi
	
class ListadoTipoMovi(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_tipomov'
	template_name = "pages/mantenimiento/tipo_movi.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_tipo_mov':
				data = []
				for i in TipoMov.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de tipos de movimientos"
		context["form"] = FormTipoMovi()
		return context
	
class RegistrarTipoMovi(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_tipo_movi':
				form = FormTipoMovi(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Tipo de movimiento registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ActualizarTipoMovi(LoginRequiredMixin, View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_tipo_movi':
				tipo_movi = TipoMov.objects.filter(id = request.POST['id']).first()
				form = FormTipoMovi(request.POST, instance=tipo_movi)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'El tipo de movimiento se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)