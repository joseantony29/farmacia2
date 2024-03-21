from django.contrib import admin
from .models import Almacen, Producto, Inventario, TipoInsumo, Laboratorio
# Register your models here.

class AlmacenAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
    # readonly_fields = ('date_of_birth',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'almacen', 'tipo_insumo', 'total_stock')
    list_filter = ('tipo_insumo', 'almacen')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    # readonly_fields = ('date_of_birth',)

class TipoInsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
    # readonly_fields = ('date_of_birth',)

class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
    # readonly_fields = ('date_of_birth',)

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'lote', 'f_vencimiento', 'stock')
    list_filter = ('producto', 'f_vencimiento')
    search_fields = ('producto',)
    ordering = ('producto', 'f_vencimiento')
    # readonly_fields = ('date_of_birth',)

admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(TipoInsumo, TipoInsumoAdmin)
admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Inventario, InventarioAdmin)