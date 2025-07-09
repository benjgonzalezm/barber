from django.shortcuts import redirect
from functools import wraps

#Función para determinar si un usuario en específico puede acceder a las secciones de la página que tiene permitido
def tipo_usuario_requerido(tipos_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            tipo_usuario = request.session.get('tipo_usuario')
            if tipo_usuario in tipos_permitidos:
                return view_func(request, *args, **kwargs)
            return redirect('404')
        return _wrapped_view
    return decorador