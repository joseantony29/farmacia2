from django.contrib import admin
from .models import Beneficiado, Perfil, Zona
# Register your models here.

class ZonaAdmin(admin.ModelAdmin):
    list_display = ('zona_residencia',)
    list_filter = ('zona_residencia',)
    search_fields = ('zona_residencia',)
    ordering = ('zona_residencia',)
    # readonly_fields = ('date_of_birth',)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'zona', 'rol')
    list_filter = ('zona',)
    search_fields = ('cedula', 'apellidos')
    date_hierarchy = 'f_nacimiento'
    ordering = ('nombres',)
    # readonly_fields = ('date_of_birth',)


class BeneficiadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'zona')
    list_filter = ('zona',)
    search_fields = ('cedula', 'apellidos')
    date_hierarchy = 'f_nacimiento'
    ordering = ('nombres',)
    # readonly_fields = ('date_of_birth',)

admin.site.register(Zona, ZonaAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Beneficiado, BeneficiadoAdmin)