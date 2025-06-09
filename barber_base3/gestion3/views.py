from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Servicio, EstadoCita, Usuario, TipoUsuario, EstadoUsuario, Cita, ValoracionObservacion 
from .models import RegistroPago, Observacion , FormaPago , Descuento
from django.contrib.auth.hashers import check_password





def perfil_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    if usuario.id_tipo_usuario.tipo == "Cliente":
        citas = Cita.objects.filter(id_cliente=usuario).select_related('id_servicio', 'id_estado_cita')
    else:
        citas = Cita.objects.filter(id_servicio__id_usuario=usuario).select_related('id_cliente', 'id_estado_cita', 'id_servicio')

    citas_info = []
    for cita in citas:
        valoraciones = ValoracionObservacion.objects.filter(id_cita=cita)
        observaciones = [v.id_observacion.nombre_observacion for v in valoraciones]
        valoracion = valoraciones.first().valoracion if valoraciones.exists() else None

        citas_info.append({
            'cita': cita,
            'valoracion': valoracion,
            'observaciones': observaciones
        })

    observaciones_disponibles = Observacion.objects.all()

    return render(request, 'gestion3/citas.html', {
        'usuario': usuario,
        'tipo_usuario': usuario.id_tipo_usuario.tipo,
        'citas_info': citas_info,
        'observaciones_disponibles': observaciones_disponibles
    })

def valorar_cita(request, cita_id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id_cita=cita_id)
        valor = int(request.POST['valoracion'])
        observaciones_ids = request.POST.getlist('observaciones')

        for obs_id in observaciones_ids:
            observacion = get_object_or_404(Observacion, id_observacion=obs_id)
            ValoracionObservacion.objects.create(
                valoracion=valor,
                id_observacion=observacion,
                id_cita=cita
            )

        messages.success(request, 'Valoración registrada exitosamente.')
        return redirect('perfil')

def finalizar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id_cita=cita_id)
    estado_finalizado = EstadoCita.objects.get(estado_cita='Finalizado')
    cita.id_estado_cita = estado_finalizado
    cita.save()
    return redirect('perfil')

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id_cita=cita_id)
    estado_cancelado = EstadoCita.objects.get(estado_cita='Cancelado')
    cita.id_estado_cita = estado_cancelado
    cita.save()
    return redirect('perfil')









def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correorelogin')
        contraseña = request.POST.get('contraseñalogin')

        try:
            usuario = Usuario.objects.get(correo=correo)
            
           
            if usuario.contraseña_hash == hashlib.sha256(contraseña.encode()).hexdigest():
         
                if usuario.id_estado_usuario.estado_usuario == 'Activo':
                 
                    request.session['usuario_id'] = usuario.id_usuario
                    request.session['usuario_nombre'] = f"{usuario.nombre} {usuario.apellido}"
                    return redirect('menu')  
                else:
                    return render(request, 'gestion3/logueate.html', {'error': 'Usuario bloqueado. Contacte con el administrador.'})
            else:
                return render(request, 'gestion3/logueate.html', {'error': 'Contraseña incorrecta'})

        except Usuario.DoesNotExist:
            return render(request, 'gestion3/logueate.html', {'error': 'Usuario no encontrado'})

    return render(request, 'gestion3/logueate.html')





def logout_view(request):
    request.session.flush() 
    return redirect('login')  





def pagina_principal(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('gestion3/logueate.html')

    usuario = Usuario.objects.get(id_usuario=usuario_id)
    return render(request, 'gestion3/menu.html', {'usuario': usuario})






def servicios(request):
    servicios_all = Servicio.objects.select_related('id_subservicio', 'id_usuario')
    servicios_unicos = {}
    for servicio in servicios_all:
        key = servicio.id_subservicio.id_subservicio  
        if key not in servicios_unicos:
            servicios_unicos[key] = servicio
    servicios = servicios_unicos.values()
    return render(request, 'gestion3/servicios.html', {'servicios': servicios})




def barbero(request, servicio_id):
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)

   
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

        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, 'Debes iniciar sesión para reservar una cita.')
            return redirect('login')

        cliente = Usuario.objects.get(id_usuario=usuario_id)

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




def registro_barbero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreregistro')
        apellido = request.POST.get('apellidoregistro')
        correo = request.POST.get('correoregistro')
        telefono = request.POST.get('celularregistro')
        contraseña = request.POST.get('contraseñaregistro')
        descripcion = request.POST.get('descripcionregistro')
        imagen = request.FILES.get('imagenperfil')


        contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()

        tipo_usuario = TipoUsuario.objects.get(tipo='Barbero')  
        estado_usuario = EstadoUsuario.objects.get(estado_usuario='Activo')


        nuevo_barbero = Usuario.objects.create(
            id_tipo_usuario=tipo_usuario,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo,
            contraseña_hash=contraseña_hash,
            descripcion_usuario=descripcion,
            imagen=imagen,
            id_estado_usuario=estado_usuario
        )

        messages.success(request, 'Barbero registrado correctamente.')
        return redirect('login')  

    return render(request, 'gestion3/registrobarbero.html')










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











def menu(request):
    return render(request, 'gestion3/menu.html')






def nosotros(request):
    return render(request, 'gestion3/nosotros.html')










def testimonios(request):
    return render(request, 'gestion3/testimonios.html')




def ver_pagos(request):
    return render(request, 'gestion3/ver_pagos.html')






def registrar_pago(request):
    cita_id = request.GET.get('cita_id')
    if not cita_id:
        messages.error(request, "ID de cita no proporcionado.")
        return redirect('perfil')

    cita = get_object_or_404(Cita, id_cita=cita_id)

    cliente = cita.id_cliente
    barbero = cita.id_servicio.id_usuario
    servicio = cita.id_servicio.id_subservicio
    monto_original = str(cita.id_servicio.precio).replace(',', '.')  # CORREGIDO
    fecha_pago = cita.fecha_cita

    formas_pago = FormaPago.objects.all()
    descuentos = Descuento.objects.filter(id_usuario=barbero)

    return render(request, 'gestion3/registro_pagos.html', {
        'cita': cita,
        'cliente': cliente,
        'barbero': barbero,
        'servicio': servicio,
        'monto_original': monto_original,
        'fecha_pago': fecha_pago,
        'formas_pago': formas_pago,
        'descuentos': descuentos
    })







def guardar_pago(request):
    if request.method == 'POST':
        cita_id = request.POST.get('cita')
        forma_pago_id = request.POST.get('forma_pago')
        descuento_valor = float(request.POST.get('descuento', 0)) / 100
        total_pagado = float(request.POST.get('total_pagado'))

        cita = get_object_or_404(Cita, id_cita=cita_id)
        forma_pago = get_object_or_404(FormaPago, id_forma_pago=forma_pago_id)
        barbero = cita.id_servicio.id_usuario

        descuento_obj = None
        if descuento_valor > 0:
            descuento_obj, _ = Descuento.objects.get_or_create(
                id_usuario=barbero,
                descuento=descuento_valor
            )

        RegistroPago.objects.create(
            id_cita=cita,
            id_forma_pago=forma_pago,
            monto_original=cita.id_servicio.precio,
            total_pagado=total_pagado,
            id_descuento=descuento_obj,
            fecha_pago=cita.fecha_cita  
        )

        messages.success(request, "Pago registrado correctamente.")
        return redirect('perfil')


