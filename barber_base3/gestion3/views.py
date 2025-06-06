from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render



def menu(request):
    return render(request, 'gestion3/menu.html')


def bloquear_usuario(request):
    return render(request, 'gestion3/bloquear_usuario.html')

def citas(request):
    return render(request, 'gestion3/citas.html')

def logueate(request):
    return render(request, 'gestion3/logueate.html')

def nosotros(request):
    return render(request, 'gestion3/nosotros.html')

def perfil_view(request):
    return render(request, 'gestion3/perfil_atenciones.html')

def registrate(request):
    return render(request, 'gestion3/registrate.html')

def registro_pagos(request):
    return render(request, 'gestion3/registro_pagos.html')

def registro_barbero(request):
    return render(request, 'gestion3/registrobarbero.html')

def selecciona_barber(request):
    return render(request, 'gestion3/selecciona-barber.html')

def servicios(request):
    return render(request, 'gestion3/servicios.html')

def testimonios(request):
    return render(request, 'gestion3/testimonios.html')

def ver_pagos(request):
    return render(request, 'gestion3/ver_pagos.html')
