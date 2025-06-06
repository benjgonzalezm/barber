from django.urls import path
from gestion3 import views
from .views import *
from . import views



urlpatterns = [
    path('', views.menu, name='menu'),
    path('citas/', views.citas, name='citas'),
    path('login/', views.logueate, name='login'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('registrate/', views.registrate, name='registrate'),
    path('registro-pagos/', views.registro_pagos, name='registro_pagos'),
    path('registro-barbero/', views.registro_barbero, name='registro_barbero'),
    path('selecciona-barber/', views.selecciona_barber, name='selecciona_barber'),
    path('servicios/', views.servicios, name='servicios'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('ver-pagos/', views.ver_pagos, name='ver_pagos'),
    path('usuarios/<int:user_id>/bloquear/', views.bloquear_usuario, name='bloquear_usuario'),
    path('usuarios/<int:user_id>/activar/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/<int:user_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
]



