
import json
from datetime import date, timedelta
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.generic import (
	TemplateView,
	ListView,
	UpdateView,
	DetailView,
	View
)
from ...forms import BeneficiadoForm, SolicitudEditForm, SolicitudPresencialForm, PerfilForm
from apps.entidades.permisos import permisos_usuarios
from apps.entidades.mixins import ValidarUsuario
from django.contrib.auth.mixins import LoginRequiredMixin

from ...models import Solicitud, TipoMov, DetalleSolicitud, Historial
from apps.inventario.models import Producto
from apps.entidades.models import Beneficiado, Perfil, User
# # Create your views here.

class SolicitudesMed(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_solicitud'
	template_name = 'pages/movimientos/solicitudes/listado_solicitudes_med.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		solicitudes = Solicitud.objects.all().order_by('-pk')

		context["sub_title"] = "Solicitudes de medicamentos"
		context['solicitudes'] = solicitudes
		return context

class DetalleSolicitudMed(ValidarUsuario, DetailView):
	template_name = 'pages/movimientos/solicitudes/detalle_solicitud_med.html'
	permission_required = 'movimientos.view_solicitud'
	model = Solicitud
	context_object_name = 'solicitud'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Detalle de Solicitud"
		return context

class EditarSolicitud(ValidarUsuario, SuccessMessageMixin, UpdateView):
	permission_required = 'movimientos.change_solicitud'
	template_name = 'pages/movimientos/solicitudes/editar_solicitud_de_med.html'
	model = Solicitud
	form_class = SolicitudEditForm
	success_massage = 'La solicitud ha sido modificada correctamente'
	# permission_required = 'anuncios.requiere_secretria'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		if request.user.perfil.rol == 'AD':
			if self.get_object().tipo_solicitud == 'PR':
				return redirect('listado_solicitudes_medicamentos')
			elif self.get_object().tipo_solicitud == 'ON':
				if self.get_object().estado in ['RE','ET','EE','AP']:
					return redirect('listado_solicitudes_medicamentos')
		if request.user.perfil.rol == "AL":
			if self.get_object().tipo_solicitud == 'PR':
				if self.get_object().estado in ['RE','ET','EE']:
					return redirect('listado_solicitudes_medicamentos')
			elif self.get_object().tipo_solicitud == 'ON':
				if self.get_object().estado in ['PR','RE','EE','ET']:
					return redirect('listado_solicitudes_medicamentos')
		return super().dispatch(request, *args, **kwargs)

	def producto_proximo_a_vencer(self, producto):
		# Obtiene la fecha actual
		hoy = date.today()
		# Busca en el inventario del producto aquellos que estén próximos a vencer
		inventarios_proximos = producto.inventario.filter(f_vencimiento__gt=hoy, stock__gt=0).order_by('f_vencimiento')
		return inventarios_proximos

	def descontar_stock(self, inventario, cantidad):

		perfil = Perfil.objects.filter(usuario=self.request.user).first()
		tipo_ingreso, created = TipoMov.objects.get_or_create(nombre='SOLICITUD DE MEDICAMENTO', operacion='-')
		movimiento = {
			'tipo_mov': tipo_ingreso,
			'perfil': perfil,
			'producto': inventario,
			'cantidad': 0
		}

		if inventario.stock >= cantidad:
			inventario.stock -= cantidad
			inventario.save()
			movimiento['cantidad'] = cantidad
			Historial().crear_movimiento(movimiento)
			return 0 # Indica que no hay cantidad restante
		else:
			restante = cantidad - inventario.stock
			movimiento['cantidad'] = inventario.stock
			inventario.stock = 0
			inventario.save()
			Historial().crear_movimiento(movimiento)
			return restante # Indica que no hay cantidad restante
		
	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])

			solicitud = self.get_object()
			solicitud.descripcion = vents['descripcion']
			solicitud.estado = vents['estado']
			solicitud.beneficiado_id = vents['beneficiado']
			# solicitud.perfil_id = vents['perfil']
			usuario = User.objects.filter(username=f'{solicitud.perfil.nacionalidad}{solicitud.perfil.cedula}').first()
			if request.FILES.get('recipe'):
				solicitud.recipe = request.FILES['recipe']

			if vents['estado'] == 'AP':
					solicitud.proceso_actual = Solicitud.FaseProceso.ALMACENISTA
			elif vents['estado'] == 'EE':
				solicitud.proceso_actual = Solicitud.FaseProceso.AT_CLIENTE

			solicitud.save()

			DetalleSolicitud.objects.filter(solicitud=self.get_object()).delete()
			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()


				detalle = DetalleSolicitud() 
				detalle.solicitud = solicitud
				detalle.producto = producto
				detalle.cant_solicitada = det['cantidad']
				detalle.cant_entregada = det['cantidad_entregada']
				detalle.save()

				if vents['estado'] == 'EE':
					cantidad_restante = det['cantidad_entregada']
					while cantidad_restante > 0:
						inventarios_proximos = self.producto_proximo_a_vencer(producto)
						if inventarios_proximos.exists():
							# Asume que se descontará del primer inventario próximo a vencer
							inventario = inventarios_proximos.first()
							cantidad_restante = self.descontar_stock(inventario, cantidad_restante)
							detalle.inventario.add(inventario)
							detalle.save()
						else:
							# Si no hay inventarios próximos a vencer, se detiene el proceso
							break
					producto.contar_productos()
					# # # enviando el correo de registro

					# # Cargar la plantilla HTML
					# html_content = render_to_string('templates/email/email_registro.html', {'correo': usuario.email, 'nombres': usuario.perfil.nombres, 'apellidos':  usuario.perfil.apellidos})
					# # Configurar el correo electrónico
					# subject, from_email, to = 'SU SOLICITUD HA SIDO PROCESADA CON EXITO', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', usuario.email
					# text_content = 'Puede ir a la sede a retirar los medicamentos solicitados.'
					# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
					# msg.attach_alternative(html_content, "text/html")
					# # Enviar el correo electrónico
					# msg.send()

			messages.success(request,'Solicitud de medicamento registrado correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Solicitud de medicamento registrado correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_detail(self):
		data = []
		try:
			for i in DetalleSolicitud.objects.filter(solicitud_id=self.get_object().id):
				item = i.producto.toJSON()
				item['cantidad'] = i.cant_solicitada
				item['cantidad_entregada'] = i.cant_entregada
				item['nombre'] = i.producto.nombre
				item['id'] = i.producto.pk
				item['text'] = i.producto.nombre
				data.append(item)
		except:
			pass
		return data

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rol'] = self.request.user.perfil.rol
		context["sub_title"] = "Modificar solicitud"
		context["form_b"] = BeneficiadoForm()
		context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
		context['tipo_solicitud'] = self.get_object().tipo_solicitud
		return context

class RegistrarSolicitudPresencial(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.add_solicitud'
	template_name = 'pages/movimientos/solicitudes/registrar_solicitud_de_med_presencial.html'
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			with transaction.atomic():
				vents = json.loads(request.POST['vents'])

				solicitud = Solicitud()
				solicitud.fecha_soli = date.today()
				solicitud.descripcion = vents['descripcion']
				solicitud.beneficiado= Beneficiado.objects.filter(cedula=vents['beneficiado']).first()
				solicitud.perfil_id = vents['perfil']
				solicitud.recipe = request.FILES['recipe']
				solicitud.proceso_actual = solicitud.FaseProceso.AT_CLIENTE
				solicitud.tipo_solicitud = solicitud.TipoSoli.PRESENCIAL
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
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar Solicitud de medimento presencial"
		context["form"] = SolicitudPresencialForm()
		context["form_b"] = BeneficiadoForm()
		context["form_p"] = PerfilForm()
		context['beneficiados'] = Beneficiado.objects.all()
		context['perfiles'] = Perfil.objects.all()
		return context

class MedicamentoEntregado(ValidarUsuario, SuccessMessageMixin, View):
	permission_required = 'entidades.cambiar_estado_solicitudes'
	success_massage = 'El medicamento ha sido entregado correctamente'
	# permission_required = 'anuncios.requiere_secretria'
	object = None
		
	def get(self, request, pk, *args, **kwargs):
		try:
			with transaction.atomic():

				solicitud = Solicitud.objects.filter(pk=pk).first()
				if solicitud:
					if request.user.perfil.rol == 'AT':
						solicitud.estado = Solicitud.Status.ENTREGADO
						solicitud.save()
						messages.success(request, self.success_massage)
					else:
						messages.error(request, 'No tienes permisos para realizar esta acción.')
				else:
					messages.error(request, 'La solicitud no existe.')
				# messages.success(request,'Solicitud de medicamento registrado correctamente')
		except Exception as e:
			messages.error(request, 'Ocurrió un error al procesar la solicitud.')
			print(e)
		return redirect('listado_solicitudes_medicamentos')
	
class RegistrarBeneficiadoFisico(LoginRequiredMixin, View):
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
				beneficiado.perfil_id = request.POST['perfil']
				beneficiado.save()
				data['response'] = {'title':'Exito!', 'data': 'El beneficiado se registro correctamente', 'type_response': 'success'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'El beneficiado ya existe', 'type_response': 'danger'}
				# 	data['response'] = {'title': 'Exito!', 'data':'Compra registrada correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class RegistrarPerfilFisico(LoginRequiredMixin, View):
	# permission_required = 'anuncios.requiere_secretria'
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			with transaction.atomic():
				if not User.objects.filter(username=f'{request.POST["nacionalidad"]}{request.POST["cedula"]}').first():
					usuario = User()
					usuario.username = f'{request.POST["nacionalidad"]}{request.POST["cedula"]}'
					usuario.email = request.POST["email"]
					usuario.set_password(request.POST["password1"])
					usuario.is_active = request.POST.get('is_active') == 'on'
					usuario.save()

					permissions = Permission.objects.filter(codename__in=permisos_usuarios[request.POST["rol"]])
					for permission in permissions:
						usuario.user_permissions.add(permission)
					usuario.save()

					perfil = Perfil()
					perfil.nacionalidad = request.POST["nacionalidad"]
					perfil.cedula = request.POST["cedula"]
					perfil.nombres = request.POST["nombres"]
					perfil.apellidos = request.POST["apellidos"]
					perfil.telefono = f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}'
					perfil.genero = request.POST["genero"]
					if request.POST["genero"] == 'MA':
						perfil.embarazada = False
					else:
						perfil.embarazada = request.POST["embarazada"]
					perfil.f_nacimiento = request.POST["f_nacimiento"]
					if request.FILES.get("c_residencia"):
						perfil.c_residencia = request.FILES.get("c_residencia")
					perfil.zona_id = request.POST["zona"]
					perfil.direccion = request.POST["direccion"]
					perfil.rol = request.POST["rol"]
					perfil.usuario = User.objects.get(username = usuario.username)
					perfil.save()


					if Beneficiado.objects.filter(cedula=perfil.cedula).first():
						beneficiado = Beneficiado.objects.filter(cedula=perfil.cedula).first()
					else:
						beneficiado = Beneficiado()
					beneficiado.perfil_id = perfil.pk
					beneficiado.nacionalidad = request.POST["nacionalidad"]
					beneficiado.cedula = request.POST["cedula"]
					beneficiado.nombres = request.POST["nombres"]
					beneficiado.apellidos = request.POST["apellidos"]
					beneficiado.telefono = f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}'
					beneficiado.genero = request.POST["genero"]
					beneficiado.f_nacimiento = request.POST["f_nacimiento"]
					if request.POST["genero"] == 'MA':
						beneficiado.embarazada = False
					else:
						beneficiado.embarazada = request.POST["embarazada"]
					if request.FILES.get("c_residencia"):
						beneficiado.c_residencia = request.FILES.get("c_residencia")
					beneficiado.zona_id = request.POST["zona"]
					beneficiado.direccion = request.POST["direccion"]
					beneficiado.save()

					# enviando el correo de registro

					# Cargar la plantilla HTML
					html_content = render_to_string('templates/email/email_registro.html', {'correo': request.POST['email'], 'nombres': request.POST['nombres'], 'apellidos': request.POST['apellidos']})
					# Configurar el correo electrónico
					subject, from_email, to = 'REGISTRO EXITOSO', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', request.POST['email']
					text_content = 'ESTE ES UN MENSAJE DE BIENVENIDA.'
					msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
					msg.attach_alternative(html_content, "text/html")
					# Enviar el correo electrónico
					msg.send()

					data['response'] = {'title':'Exito!', 'data': 'El titular se registro correctamente', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'El titular ya existe', 'type_response': 'danger'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)