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
]
