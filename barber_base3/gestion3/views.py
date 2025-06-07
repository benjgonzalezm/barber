from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Servicio, EstadoCita, Usuario, TipoUsuario, EstadoUsuario, Cita, ValoracionObservacion




def servicios(request):
    servicios_all = Servicio.objects.select_related('id_subservicio', 'id_usuario')
    servicios_unicos = {}
    for servicio in servicios_all:
        key = servicio.id_subservicio.id_subservicio  # id del subservicio
        if key not in servicios_unicos:
            servicios_unicos[key] = servicio
    servicios = servicios_unicos.values()
    return render(request, 'gestion3/servicios.html', {'servicios': servicios})




def barbero(request, servicio_id):
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)

    # Obtengo los barberos y también el servicio de cada barbero relacionado a este subservicio
    barberos_con_servicio = Servicio.objects.filter(
        id_subservicio=servicio.id_subservicio,
        id_usuario__id_tipo_usuario__tipo='Barbero'
    ).select_related('id_usuario')

    return render(request, 'gestion3/barbero.html', {
        'servicio': servicio,
        'barberos_con_servicio': barberos_con_servicio
    })



def reservar(request, servicio_id, barbero_id):
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)
    barbero = get_object_or_404(Usuario, id_usuario=barbero_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        estado_cita = EstadoCita.objects.get(estado_cita='En progreso')
        cliente = Usuario.objects.get(id_usuario=2)  # por ahora fijo como dijiste

        nueva_cita = Cita.objects.create(
            id_cliente=cliente,
            id_servicio=servicio,
            id_estado_cita=estado_cita,
            fecha_cita=fecha,
            hora_cita=hora
        )

        messages.success(request, 'Cita reservada correctamente.')
        return redirect('menu')

    return render(request, 'gestion3/reservar.html', {
        'servicio': servicio,
        'barbero': barbero
    })







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





def testimonios(request):
    return render(request, 'gestion3/testimonios.html')

def ver_pagos(request):
    return render(request, 'gestion3/ver_pagos.html')



