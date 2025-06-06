from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, TipoUsuario, EstadoUsuario
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cita, ValoracionObservacion






@csrf_exempt
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(pk=user_id)
            usuario.delete()
            return JsonResponse({'success': True})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@csrf_exempt
def bloquear_usuario(request, user_id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, id_usuario=user_id)
        estado_bloqueado = EstadoUsuario.objects.get(estado_usuario='Bloqueado')
        usuario.id_estado_usuario = estado_bloqueado
        usuario.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@csrf_exempt
def activar_usuario(request, user_id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, id_usuario=user_id)
        estado_activo = EstadoUsuario.objects.get(estado_usuario='Activo')
        usuario.id_estado_usuario = estado_activo
        usuario.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestion3/bloquear_usuario.html', {'usuarios': usuarios})







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







def registro_citas(request):
    citas = Cita.objects.all()
    citas_con_valoracion = []

    for cita in citas:
        observaciones = ValoracionObservacion.objects.filter(id_cita=cita)

        if observaciones.exists():
            valoracion = observaciones.first().valoracion
          
            observaciones_list = [obs.id_observacion.nombre_observacion for obs in observaciones]
        else:
            valoracion = None
            observaciones_list = []

        citas_con_valoracion.append({
            'cita': cita,
            'valoracion': valoracion,
            'observaciones': observaciones_list
        })

    return render(request, 'gestion3/registro_citas.html', {
        'citas_con_valoracion': citas_con_valoracion
    })













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
