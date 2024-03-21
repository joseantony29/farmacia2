from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class ValidarUsuario(LoginRequiredMixin, UserPassesTestMixin):
	permission_required = None
	redirect_url = '/inicio/'

	def test_func(self):
		return self.request.user.has_perm(self.permission_required)

	def handle_no_permission(self):
		if not self.request.user.has_perm(self.permission_required):
			messages.error(self.request, 'No tienes permisos para acceder a esta página.')
			return redirect(self.redirect_url)

		return super().handle_no_permission()

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect('/ingresar/')
		return super().dispatch(request, *args, **kwargs)