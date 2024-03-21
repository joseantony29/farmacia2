
import json
from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.views.generic import (
	TemplateView,
	ListView,
	CreateView,
	DetailView,
	View
)
from apps.entidades.mixins import ValidarUsuario
from django.contrib.auth.mixins import LoginRequiredMixin

from ...forms import MiSolicitudForm, BeneficiadoForm

from ...models import Solicitud, TipoMov, DetalleSolicitud, Historial
from apps.inventario.models import Inventario, Producto
from apps.entidades.models import Beneficiado,Perfil
# # Create your views here.

class MisSolicitudesMedOnline(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_mis_solicitudes_de_medicamentos'
	template_name = 'pages/movimientos/solicitudes_online/listado_solicitudes_med_online.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		mis_solicitudes = Solicitud.objects.filter(perfil__cedula=self.request.user.perfil.cedula).order_by('-pk')
		print(mis_solicitudes)
		context["sub_title"] = "Mis Solicitudes online"	
		context['solicitudes'] = mis_solicitudes
		return context

class DetalleMiSolicitudOnline(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_mis_solicitudes_de_medicamentos'
	template_name = 'pages/movimientos/solicitudes_online/detalle_solicitud_med_online.html'
	# permission_required = 'anuncios.requiere_secretria'

	def get(self, request, pk, *args, **kwargs):
		context = {}
		try:
			mi_solicitud = Solicitud.objects.get(pk=pk, perfil=request.user.perfil)
			context['solicitud'] = mi_solicitud
			context["sub_title"] = "Detalle de mi solicitud"
			return render(request, self.template_name, context)
		except Solicitud.DoesNotExist:
			return redirect('mis_solicitudes_medicamentos')
	
class RegistrarMiSolicitud(ValidarUsuario, TemplateView):
	permission_required = 'entidades.registrar_mi_solicitud_de_medicamentos'
	template_name = 'pages/movimientos/solicitudes_online/registrar_mi_solicitud_de_med.html'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])
			print(vents['beneficiado'], request.user.perfil.pk)
			solicitud = Solicitud()
			solicitud.fecha_soli = date.today()
			solicitud.descripcion = vents['descripcion']
			solicitud.beneficiado_id = vents['beneficiado']
			solicitud.perfil_id = request.user.perfil.pk
			solicitud.recipe = request.FILES['recipe']
			solicitud.proceso_actual = solicitud.FaseProceso.AT_CLIENTE
			solicitud.tipo_solicitud = solicitud.TipoSoli.ONLINE
			solicitud.estado = solicitud.Status.EN_PROCRESO 
			solicitud.save()

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()

				detalle = DetalleSolicitud()
				detalle.solicitud = solicitud
				detalle.producto = producto
				detalle.cant_solicitada = det['cantidad']
				detalle.save()

			messages.success(request,'Solicitud de medicamento registrado correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Solicitud de medicamento registrado correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar ingreso"
		context["form"] = MiSolicitudForm(user=self.request.user)
		context["form_b"] = BeneficiadoForm()
		return context
	
class RegistrarBeneficiado(LoginRequiredMixin, View):
	# permission_required = 'anuncios.requiere_secretria'
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			if not Beneficiado.objects.filter(cedula=request.POST['cedula']):
				beneficiado = Beneficiado()
				beneficiado.nacionalidad = request.POST['nacionalidad'] 
				beneficiado.cedula = request.POST['cedula'] 
				beneficiado.nombres = request.POST['nombres'] 
				beneficiado.apellidos = request.POST['apellidos']
				beneficiado.telefono = f"{request.POST['codigo_tlf']}{request.POST['telefono']}"
				beneficiado.genero = request.POST['genero'] 
				if request.POST["genero"] == 'MA':
					beneficiado.embarazada = False
				else:
					beneficiado.embarazada = request.POST["embarazada"]
				beneficiado.f_nacimiento = request.POST['f_nacimiento'] 
				beneficiado.zona_id = request.POST['zona'] 
				beneficiado.direccion = request.POST['direccion']
				beneficiado.perfil_id = request.user.perfil.pk
				beneficiado.save()
				data['response'] = {'title':'Exito!', 'data': 'El beneficiado se registro correctamente', 'type_response': 'success'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'El beneficiado ya existe', 'type_response': 'danger'}
				# 	data['response'] = {'title': 'Exito!', 'data':'Compra registrada correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
