from django.contrib import admin
from django.urls import path
from productos import views




urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login_view),
    path('dashboard/', views.dashboard),
    path('change/', views.change),
    path('change/<username>/', views.change),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('carrito/', views.carrito, name='carrito'),
    path('confirmacion_pago/', views.confirmacion_pago, name='confirmacion_pago'),
    path('crear_productos/', views.crear_productos, name='crear_productos'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('mostrar_boleta/<int:boleta_id>/', views.mostrar_boleta, name='mostrar_boleta'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'), 
    path('detalle_boleta/<int:boleta_id>/', views.detalle_boleta, name='detalle_boleta'),
    path('usuario/<str:username>/', views.detalles_usuario, name='detalles_usuario'),
    path('confirmar_eliminacion_usuario/<str:username>/', views.confirmar_eliminacion_usuario, name='confirmar_eliminacion_usuario'),
    path('confirmar-eliminar-producto/<int:item_id>/', views.confirmar_eliminar_producto, name='confirmar_eliminar_producto'),
    path('gestion_productos', views.gestion_productos, name='gestion_productos'),
     path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('confirmar-eliminar-gestion/<int:producto_id>/', views.confirmar_eliminar_gestion, name='confirmar_eliminar_gestion'),
]
