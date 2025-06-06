from django.db import models

# Create your models here.

class TipoUsuario(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True)
    TIPO_CHOICES = [
        ('Barbero', 'Barbero'),
        ('Cliente', 'Cliente'),
        ('Barbería', 'Barbería'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.tipo

class EstadoUsuario(models.Model):
    id_estado_usuario = models.AutoField(primary_key=True)
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Bloqueado', 'Bloqueado'),
    ]
    estado_usuario = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.estado_usuario

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    contraseña_hash = models.CharField(max_length=255)
    descripcion_usuario = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    id_estado_usuario = models.ForeignKey(EstadoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    duracion_minutos = models.PositiveIntegerField()
    precio = models.FloatField()

    def __str__(self):
        return self.nombre_servicio

class EstadoCita(models.Model):
    id_estado_cita = models.AutoField(primary_key=True)
    ESTADO_CITA_CHOICES = [
        ('En progreso', 'En progreso'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado'),
    ]
    estado_cita = models.CharField(max_length=20, choices=ESTADO_CITA_CHOICES)

    def __str__(self):
        return self.estado_cita

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas_cliente')
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_estado_cita = models.ForeignKey(EstadoCita, on_delete=models.CASCADE)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()

    def __str__(self):
        return f"Cita {self.id_cita} - {self.fecha_cita} {self.hora_cita}"

class FormaPago(models.Model):
    id_forma_pago = models.AutoField(primary_key=True)
    FORMA_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Débito', 'Débito'),
        ('Crédito', 'Crédito'),
    ]
    nombre_forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES)

    def __str__(self):
        return self.nombre_forma_pago

class Descuento(models.Model):
    id_descuento = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descuento = models.FloatField()

    def __str__(self):
        return f"{self.descuento}% para Usuario {self.id_usuario}"

class RegistroPago(models.Model):
    id_registro_pago = models.AutoField(primary_key=True)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    id_forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    monto_original = models.FloatField()
    total_pagado = models.FloatField()
    id_descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_pago = models.DateTimeField()

    def __str__(self):
        return f"Pago {self.id_registro_pago} - Cita {self.id_cita} - Total monto {self.total_pagado}"

class Observacion(models.Model):
    id_observacion = models.AutoField(primary_key=True)
    OBSERVACION_CHOICES = [
        ('Puntualidad', 'Puntualidad'),
        ('Trato', 'Trato'),
        ('Servicio', 'Servicio'),
        ('Barbero', 'Barbero'),
    ]
    nombre_observacion = models.CharField(max_length=20, choices=OBSERVACION_CHOICES)

    def __str__(self):
        return self.nombre_observacion

class ValoracionObservacion(models.Model):
    id_valoracion_observacion = models.AutoField(primary_key=True)
    valoracion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    id_observacion = models.ForeignKey(Observacion, on_delete=models.CASCADE)
    id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE)

    def __str__(self):
        return f"Valoración {self.valoracion} - Cita {self.id_cita}"

class Bitacora(models.Model):
    id_bitacora = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_accion = models.TextField()
    fecha_bitacora = models.DateTimeField()
    tipo_accion = models.CharField(max_length=100)

    def __str__(self):
        return f"Bitácora {self.id_bitacora} - Usuario {self.id_usuario}"