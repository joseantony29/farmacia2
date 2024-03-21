from django.urls import path

from .views import (
    ListadoProductos,
    DetalleProductoView, 
    ListadoLaboratorio, 
    RegistrarLab, 
    ListadoTiposInsumos, 
    ListadoAlmacen, 
    ActualizarLaboratorio,
    RegistrarTipoInsu,
    ActualizarTipoInsumo,
    RegistrarAlmacen,
    ActualizarAlmacen,
    RegistrarProducto,
    ActualizarProducto
)

urlpatterns = [
    path('listado-de-productos/', ListadoProductos.as_view(), name='listado_productos'),
    path('registro-de-productos/', RegistrarProducto.as_view(), name='nuevo_producto'),
    path('actualizar-producto/', ActualizarProducto.as_view(), name='editar_producto'),
    path('detalle-de-producto/<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),

    # mantenimiento
    path('listado-de-laboratorios/', ListadoLaboratorio.as_view(), name='listado_lab'),
    path('registro-de-laboratorio/', RegistrarLab.as_view(), name='nuevo_lab'),
    path('actualizar-laboratorio/', ActualizarLaboratorio.as_view(), name='edit_lab'),

    path('listado-de-insumos/', ListadoTiposInsumos.as_view(), name='listado_insumos'),
    path('registro-de-tipos-de-insumos/', RegistrarTipoInsu.as_view(), name='nuevo_t_insu'),
    path('actualizar-tipos-de-insumos/', ActualizarTipoInsumo.as_view(), name='edit_t_insu'),

    path('listado-de-almacenes/', ListadoAlmacen.as_view(), name='listado_almacen'),
    path('registro-de-almacen/', RegistrarAlmacen.as_view(), name='nuevo_almacen'),
    path('actualizar-almacen/', ActualizarAlmacen.as_view(), name='edit_almacen'),
]
