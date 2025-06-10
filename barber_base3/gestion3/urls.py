from django.urls import path
from gestion3 import views
from .views import *
from . import views




urlpatterns = [
    path('', views.menu, name='menu'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('registrate/', views.registrate, name='registrate'),
    path('registro-barbero/', views.registro_barbero, name='registro_barbero'),
    path('servicios/', views.servicios, name='servicios'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('ver-pagos/', views.ver_pagos, name='ver_pagos'),
    path('usuarios/<int:user_id>/bloquear/', views.bloquear_usuario, name='bloquear_usuario'),
    path('usuarios/<int:user_id>/activar/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/<int:user_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('registro_citas/', views.registro_citas, name='registro_citas'),
    path('barbero/<int:servicio_id>/', views.barbero, name='barbero'),
    path('reservar/<int:servicio_id>/<int:barbero_id>/', views.reservar, name='reservar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pagina_principal/', views.pagina_principal, name='pagina_principal'),  



    path('perfil/', views.perfil_view, name='perfil'),
    path('valorar_cita/<int:cita_id>/', views.valorar_cita, name='valorar_cita'),
    path('finalizar_cita/<int:cita_id>/', views.finalizar_cita, name='finalizar_cita'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),

    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),
    path('guardar_pago/', views.guardar_pago, name='guardar_pago'),


]





