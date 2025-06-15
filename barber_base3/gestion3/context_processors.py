from gestion3.models import Usuario

def tipo_usuario_context(request):
    tipo_usuario = None
    if request.session.get('usuario_id'):
        try:
            usuario = Usuario.objects.get(id_usuario=request.session['usuario_id'])
            tipo_usuario = usuario.id_tipo_usuario.tipo
        except Usuario.DoesNotExist:
            pass
    return {'tipo_usuario': tipo_usuario}
