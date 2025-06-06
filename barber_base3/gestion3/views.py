from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, TipoUsuario, EstadoUsuario
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
import hashlib

def registrate(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreregistro')
        apellido = request.POST.get('apellidoregistro')
        correo = request.POST.get('correoregistro')
        telefono = request.POST.get('celularregistro')
        contraseña = request.POST.get('contraseñaregistro')
        imagen = request.FILES.get('imagenperfil')

        # aca la contraseña se hace seguro segun dijeron los profes o nos pidieron
        contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()


        tipo_usuario = TipoUsuario.objects.get(tipo='Cliente')  
        estado_usuario = EstadoUsuario.objects.get(estado_usuario='Activo')

        nuevo_usuario = Usuario.objects.create(
            id_tipo_usuario=tipo_usuario,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo,
            contraseña_hash=contraseña_hash,
            imagen=imagen,
            id_estado_usuario=estado_usuario
        )

        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('login')  

    return render(request, 'gestion3/registrate.html')





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
