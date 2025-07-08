from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Servicio, EstadoCita, Usuario, TipoUsuario, EstadoUsuario, Cita, ValoracionObservacion 
from .models import RegistroPago, Observacion , FormaPago , Descuento,SubServicio
from django.contrib.auth.hashers import check_password
from datetime import datetime
from django.db.models import Count, Sum, Avg
from django.db.models.functions import ExtractMonth
import locale
import calendar

locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') # Permite establecer la configuración regional, para así trabajar con la moneda chilena 

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

        pago_realizado = RegistroPago.objects.filter(id_cita=cita).exists()

        citas_info.append({
            'cita': cita,
            'valoracion': valoracion,
            'observaciones': observaciones,
            'pago_realizado': pago_realizado
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
    subservicios = SubServicio.objects.all()
    return render(request, 'gestion3/servicios.html', {'subservicios': subservicios})



def barbero(request, subservicio_id):
    subservicio = get_object_or_404(SubServicio, id_subservicio=subservicio_id)

    barberos_con_servicio = Servicio.objects.filter(
        id_subservicio=subservicio,
        id_usuario__id_tipo_usuario__tipo='Barbero'
    ).select_related('id_usuario')

    return render(request, 'gestion3/barbero.html', {
        'subservicio': subservicio,
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


def registrar_pago(request):
    cita_id = request.GET.get('cita_id')
    if not cita_id:
        messages.error(request, "ID de cita no proporcionado.")
        return redirect('perfil')

    cita = get_object_or_404(Cita, id_cita=cita_id)

    cliente = cita.id_cliente
    barbero = cita.id_servicio.id_usuario
    servicio = cita.id_servicio.id_subservicio
    monto_original = str(cita.id_servicio.precio).replace(',', '.')  

   
    fecha_pago = datetime.combine(cita.fecha_cita, cita.hora_cita)

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
        descuento_valor = float(request.POST.get('descuento', 0))  
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

       
        fecha_pago = datetime.combine(cita.fecha_cita, cita.hora_cita)

        RegistroPago.objects.create(
            id_cita=cita,
            id_forma_pago=forma_pago,
            monto_original=cita.id_servicio.precio,
            total_pagado=total_pagado,
            id_descuento=descuento_obj,
            fecha_pago=fecha_pago  
        )

        messages.success(request, "Pago registrado correctamente.")
        return redirect('perfil')


def ver_pagos(request):
    pagos = RegistroPago.objects.select_related(
        'id_cita', 'id_forma_pago', 'id_descuento'
    ).all()
    return render(request, 'gestion3/ver_pagos.html', {'pagos': pagos})

def reporte(request):
    pagos = RegistroPago.objects.all()

    # Formas de pago
    formas_pago = pagos.values('id_forma_pago__nombre_forma_pago') \
                       .annotate(total=Count('id_forma_pago')) \
                       .order_by('-total')

    labels_fp = [fp['id_forma_pago__nombre_forma_pago'] for fp in formas_pago]
    data_fp = [fp['total'] for fp in formas_pago]

    # Mes con más ingresos
    ingresos_por_mes = pagos.annotate(mes=ExtractMonth('fecha_pago')) \
                        .values('mes') \
                        .annotate(total=Sum('total_pagado')) \
                        .order_by('-total')

    labels_meses = [calendar.month_name[item['mes']].capitalize() for item in ingresos_por_mes]
    data_meses = [float(item['total']) for item in ingresos_por_mes]

    # Barbero populares (por citas)
    barberos_por_cita = pagos.values(
        'id_cita__id_servicio__id_usuario__nombre',
        'id_cita__id_servicio__id_usuario__apellido'
    ).annotate(total=Count('id_cita__id_servicio__id_usuario')) \
     .order_by('-total')[:5]

    labels_barberos_citas = [f"{b['id_cita__id_servicio__id_usuario__nombre']} {b['id_cita__id_servicio__id_usuario__apellido']}" for b in barberos_por_cita]
    data_barberos_citas = [b['total'] for b in barberos_por_cita]

    # Barbero con mejores calificaciones
    valoraciones_prom = ValoracionObservacion.objects.values(
    'id_cita__id_servicio__id_usuario__nombre',
    'id_cita__id_servicio__id_usuario__apellido'
    ).annotate(promedio=Avg('valoracion')).order_by('-promedio')[:5]

    labels_barberos_val = [
        f"{v['id_cita__id_servicio__id_usuario__nombre']} {v['id_cita__id_servicio__id_usuario__apellido']}"
        for v in valoraciones_prom
    ]
    data_barberos_val = [round(v['promedio'], 2) for v in valoraciones_prom]

    # Servicios más escogidos
    servicios = pagos.values('id_cita__id_servicio__id_subservicio__nombre_servicio') \
                     .annotate(total=Count('id_cita__id_servicio')) \
                     .order_by('-total')[:5]

    labels_servicios = [s['id_cita__id_servicio__id_subservicio__nombre_servicio'] for s in servicios]
    data_servicios = [s['total'] for s in servicios]

    # Barbero que más ingresos generó
    ingresos_por_barbero = pagos.values(
        'id_cita__id_servicio__id_usuario__nombre',
        'id_cita__id_servicio__id_usuario__apellido'
    ).annotate(total=Sum('total_pagado')).order_by('-total')[:5]

    labels_barberos_ingresos = [f"{b['id_cita__id_servicio__id_usuario__nombre']} {b['id_cita__id_servicio__id_usuario__apellido']}" for b in ingresos_por_barbero]
    data_barberos_ingresos = [float(b['total']) for b in ingresos_por_barbero]

    context = {
        'labels_fp': labels_fp,
        'data_fp': data_fp,
        'labels_meses': labels_meses,
        'data_meses': data_meses,
        'labels_barberos_citas': labels_barberos_citas,
        'data_barberos_citas': data_barberos_citas,
        'labels_barberos_val': labels_barberos_val,
        'data_barberos_val': data_barberos_val,
        'labels_servicios': labels_servicios,
        'data_servicios': data_servicios,
        'labels_barberos_ingresos': labels_barberos_ingresos,
        'data_barberos_ingresos': data_barberos_ingresos,
    }

    return render(request, 'gestion3/reporte.html', context)



def agregar_servicio(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    subservicios = SubServicio.objects.all()

    if request.method == 'POST':
        id_subservicio = request.POST.get('subservicio')
        descripcion = request.POST.get('descripcion')
        duracion = int(request.POST.get('duracion'))
        precio = float(request.POST.get('precio'))

        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
        subservicio = get_object_or_404(SubServicio, id_subservicio=id_subservicio)

        Servicio.objects.create(
            id_usuario=usuario,
            id_subservicio=subservicio,
            descripcion=descripcion,
            duracion_minutos=duracion,
            precio=precio
        )

        messages.success(request, 'Servicio agregado correctamente.')
        return redirect('perfil')

    return render(request, 'gestion3/agregar_servicios.html', {'subservicios': subservicios})






def agregar_subservicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        imagen = request.FILES.get('imagen')

        if not nombre:
            messages.error(request, "El nombre es obligatorio.")
            return render(request, 'gestion3/agregar_subservicio.html')

        nuevo_subservicio = SubServicio.objects.create(
            nombre_servicio=nombre,
            imagenes=imagen
        )
        messages.success(request, "Subservicio agregado correctamente.")
        return redirect('perfil')  # O adonde quieras volver

    return render(request, 'gestion3/agregar_subservicio.html')
