from django.contrib import admin

# Register your models here.

from .models import FormaPago, RegistroPago, Cita, ValoracionObservacion, Descuento, Observacion, EstadoCita, SubServicio, Servicio, Usuario, EstadoUsuario, TipoUsuario, Bitacora

# Clases para ver en la página de admin las tablas con sus campos

class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ('id_forma_pago','nombre_forma_pago')

class RegistroPagoAdmin(admin.ModelAdmin):
    list_display = ('id_registro_pago','monto_original','id_descuento','total_pagado','fecha_pago','id_cita','id_forma_pago')

class CitaAdmin(admin.ModelAdmin):
    list_display = ('id_cita','fecha_cita','hora_cita','id_cliente','id_estado_cita','id_servicio')

class ValoracionObservacionAdmin(admin.ModelAdmin):
    list_display = ('id_valoracion_observacion','valoracion','id_cita','id_observacion')

class DescuentoAdmin(admin.ModelAdmin):
    list_display = ('id_descuento','descuento','id_usuario')

class ObservacionAdmin(admin.ModelAdmin):
    list_display = ('id_observacion','nombre_observacion')

class EstadoCitaAdmin(admin.ModelAdmin):
    list_display = ('id_estado_cita','estado_cita')
    
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio','id_subservicio','descripcion','duracion_minutos','precio','id_usuario')

class SubservicioAdmin(admin.ModelAdmin):
    list_display = ('id_subservicio','nombre_servicio','imagenes')
    
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario','nombre','apellido','telefono','correo','contraseña_hash','descripcion_usuario','imagen','id_estado_usuario','id_tipo_usuario')
    
class EstadoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_estado_usuario','estado_usuario')
    
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_usuario','tipo')
    
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('id_bitacora','descripcion_accion','fecha_bitacora','tipo_accion','id_usuario')

#Ver registros de tablas en la página de admin 

admin.site.register(FormaPago, FormaPagoAdmin)
admin.site.register(RegistroPago, RegistroPagoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ValoracionObservacion, ValoracionObservacionAdmin)
admin.site.register(Descuento, DescuentoAdmin)
admin.site.register(Observacion, ObservacionAdmin)
admin.site.register(EstadoCita, EstadoCitaAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(SubServicio, SubservicioAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(EstadoUsuario, EstadoUsuarioAdmin)
admin.site.register(TipoUsuario, TipoUsuarioAdmin)
admin.site.register(Bitacora, BitacoraAdmin)
