from django.shortcuts import render, redirect
from django.contrib import messages
from Negocio.models import Usuario  # Asegúrate de usar el modelo correcto
from utils import get_color_scheme
from .models import Pedido
from .models import Detalle_Producto
from django.http import JsonResponse
import json
import os
from django.conf import settings
from collections import defaultdict

# Vista para mostrar el formulario de inicio de sesión y procesar la validación
def login_repartidor(request):
    color_scheme = get_color_scheme()
    if request.method == "POST":
        correo = request.POST.get('usuarioRepartidor')
        password = request.POST.get('passwordRepartidor')

        if not correo or not password:  # Verifica si los campos están vacíos
            messages.error(request, 'Por favor ingresa todos los datos.')
            return render(request, 'repartidor/login_repartidor.html', {"color_scheme": color_scheme})

        try:
            usuario = Usuario.objects.get(correo=correo, password_usuario=password)
            if usuario.rol_usuario == "Administrador Repartidor":  # Verificar si el rol es "Repartidor"
                # Activar al repartidor automáticamente
                usuario.estado_usuario = True
                usuario.save()

                # Guardar datos en sesión
                request.session['correo_usuario'] = usuario.correo
                request.session['nombre_usuario'] = usuario.nombre_usuario
                request.session['rol_usuario'] = usuario.rol_usuario
                request.session['estado_usuario'] = usuario.estado_usuario  # Guardar estado en sesión

                return redirect('pedidos_asignados')  # Redirigir a la vista de pedidos asignados
            else:
                messages.error(request, 'No tienes permisos para acceder como Repartidor.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')

    # Renderizar el formulario de inicio de sesión en caso de error o método GET
    return render(request, 'repartidor/login_repartidor.html', {"color_scheme": color_scheme})



# Vista para cerrar sesión
def cerrar_sesion(request):
    correo_usuario = request.session.get('correo_usuario')
    if correo_usuario:
        try:
            # Cambiar el estado del repartidor a inactivo
            usuario = Usuario.objects.get(correo=correo_usuario)
            if usuario.rol_usuario == "Administrador Repartidor":
                usuario.estado_usuario = False
                usuario.save()
        except Usuario.DoesNotExist:
            pass  # Si no existe el usuario, ignorar

    # Eliminar la sesión
    request.session.flush()  # Elimina toda la sesión
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login_repartidor')



# Vista para activar el repartidor
def activar_repartidor(request):
    if request.method == 'POST':
        correo_usuario = request.session.get('correo_usuario')
        try:
            usuario = Usuario.objects.get(correo=correo_usuario)
            usuario.estado_usuario = True
            usuario.save()
            request.session['estado_usuario'] = True  # Actualizar el estado en sesión
            return JsonResponse({'success': True, 'message': 'Repartidor activado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No se encontró el usuario.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

# Vista para desactivar el repartidor
def desactivar_repartidor(request):
    if request.method == 'POST':
        correo_usuario = request.session.get('correo_usuario')
        try:
            usuario = Usuario.objects.get(correo=correo_usuario)
            usuario.estado_usuario = False
            usuario.save()
            request.session['estado_usuario'] = False  # Actualizar el estado en sesión
            return JsonResponse({'success': True, 'message': 'Repartidor desactivado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No se encontró el usuario.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# Vista para mostrar pedidos asignados
def pedidos_asignados(request):
    # Verificar si la sesión está activa
    if 'correo_usuario' not in request.session:
        return redirect('login_repartidor')

    # Obtener el correo del repartidor desde la sesión
    correo_repartidor = request.session.get('correo_usuario')
    nombre_usuario = request.session.get('nombre_usuario', 'Usuario')

    try:
        # Obtener el usuario repartidor
        usuario = Usuario.objects.get(correo=correo_repartidor)
        repartidor_activo = usuario.estado_usuario  # Obtener estado del repartidor
    except Usuario.DoesNotExist:
        return redirect('login_repartidor')

    # Obtener pedidos asignados para el repartidor logueado
    pedidos_asignados = Pedido.objects.filter(
        estado_pedido="asignado",
        correo=usuario  # Filtrar por el repartidor logueado
    ).select_related('id_direccion__cliente')  # Optimizar relaciones

    # Obtener esquema de colores
    color_scheme = get_color_scheme()

    return render(request, 'repartidor/pedidos_asignados.html', {
        "nombre_usuario": nombre_usuario,
        "color_scheme": color_scheme,
        "pedidos_asignados": pedidos_asignados,
        "repartidor_activo": repartidor_activo,
    })

def perfil_usuario(request):
    # Obtener el usuario logeado desde la sesión
    correo_usuario = request.session.get('correo_usuario')
    if not correo_usuario:
        return redirect('login_repartidor')  # Redirigir al login si no está autenticado

    user = Usuario.objects.get(correo=correo_usuario)

    if request.method == "POST":
        # Verificar si se sube una nueva imagen
        if request.FILES.get('imagen'):
            # Verificar si la imagen actual no es la predeterminada
            if user.imagen and os.path.basename(user.imagen.name) != 'usuario_defecto.png':
                # Eliminar la imagen anterior si existe
                imagen_path = os.path.join(settings.MEDIA_ROOT, str(user.imagen))
                if os.path.isfile(imagen_path):
                    os.remove(imagen_path)

            # Guardar la nueva imagen
            user.imagen = request.FILES['imagen']

        # Actualizar otros datos del usuario
        user.nombre_usuario = request.POST.get('nombre_usuario', user.nombre_usuario)
        if request.POST.get('password_usuario'):
            user.password_usuario = request.POST.get('password_usuario')

        user.save()

        # Actualizar nombre en sesión
        request.session['nombre_usuario'] = user.nombre_usuario

        # Responder con éxito para AJAX
        return JsonResponse({'success': True, 'message': 'Cambios guardados exitosamente.', 'nombre_usuario': user.nombre_usuario})

    return render(request, 'repartidor/perfil.html', {"user": user})

def asignar_pedido_a_repartidor(request, pedido_id):
    if request.method == 'POST':
        correo_usuario = request.session.get('correo_usuario')
        if not correo_usuario:
            return JsonResponse({'success': False, 'message': 'No estás autenticado.'})

        try:
            usuario = Usuario.objects.get(correo=correo_usuario)
            if not usuario.estado_usuario:
                return JsonResponse({'success': False, 'message': 'Debes estar activo para asignar pedidos.'})

            pedido = Pedido.objects.get(id_pedido=pedido_id, estado_pedido="pendiente")
            pedido.estado_pedido = "asignado"
            pedido.correo_id = correo_usuario
            pedido.save()

            return JsonResponse({'success': True, 'message': 'Pedido asignado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado.'})
        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El pedido no existe o ya está asignado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})




def obtener_detalle_pedido(request, pedido_id):
    if request.method == 'GET':
        try:
            pedido = Pedido.objects.get(id_pedido=pedido_id)
            detalles = Detalle_Producto.objects.filter(id_pedido_id=pedido_id).select_related('id_producto').values(
                'id_producto__nombre_producto',
                'cantidad_detalle',
                'id_producto__precio_producto'
            )

            # Agrupar los productos por nombre
            productos_agrupados = defaultdict(lambda: {'cantidad': 0, 'precio_unitario': 0, 'total': 0})
            total_pedido = 0

            for detalle in detalles:
                nombre_producto = detalle['id_producto__nombre_producto']
                cantidad = detalle['cantidad_detalle']
                precio_unitario = detalle['id_producto__precio_producto']
                total = cantidad * precio_unitario

                # Sumar cantidades y totales para productos del mismo tipo
                productos_agrupados[nombre_producto]['cantidad'] += cantidad
                productos_agrupados[nombre_producto]['precio_unitario'] = precio_unitario
                productos_agrupados[nombre_producto]['total'] += total
                total_pedido += total

            # Convertir el resultado a una lista
            detalles_con_totales = [
                {
                    'nombre_producto': nombre,
                    'cantidad': data['cantidad'],
                    'precio_unitario': data['precio_unitario'],
                    'total': data['total']
                }
                for nombre, data in productos_agrupados.items()
            ]

            response = {
                'success': True,
                'detalles': detalles_con_totales,
                'total_pedido': total_pedido
            }

            return JsonResponse(response)

        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El pedido no existe.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def entregar_pedido(request, pedido_id):
    if request.method == 'POST':
        try:
            # Obtener el pedido con el ID
            pedido = Pedido.objects.get(id_pedido=pedido_id)

            # Verificar el estado actual
            if pedido.estado_pedido == "entregado":
                return JsonResponse({'success': False, 'message': 'El pedido ya fue entregado.'})

            # Cambiar el estado del pedido a "entregado"
            pedido.estado_pedido = "entregado"
            pedido.save()

            return JsonResponse({'success': True, 'message': 'El pedido ha sido entregado exitosamente.'})
        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El pedido no existe.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})




def listar_pedidos_pendientes(request):
    if request.method == 'GET':
        try:
            # Filtrar pedidos con estado "pendiente" y obtener relaciones
            pedidos = Pedido.objects.filter(estado_pedido="pendiente").select_related(
                'id_direccion__cliente'
            ).values(
                'id_pedido',
                'id_direccion__cliente__nombre_cliente',
                'id_direccion__numero_casa',
                'id_direccion__calle',
                'id_direccion__punto_referencia',
                'id_direccion__municipio',
                'id_direccion__departamento',
                'id_direccion__nombre_direccion'
            )

            # Formatear datos para el modal
            pedidos_formateados = []
            for pedido in pedidos:
                direccion = (
                    f"Casa #{pedido['id_direccion__numero_casa']}, Calle {pedido['id_direccion__calle']}, "
                    f"Referencia: {pedido['id_direccion__punto_referencia']}, Municipio: {pedido['id_direccion__municipio']}, "
                    f"Departamento: {pedido['id_direccion__departamento']}"
                )

                pedidos_formateados.append({
                    'id_pedido': pedido['id_pedido'],
                    'nombre_cliente': pedido['id_direccion__cliente__nombre_cliente'],
                    'direccion': direccion,
                })

            return JsonResponse({'success': True, 'pedidos': pedidos_formateados})
        except Exception as e:
            print("Error al consultar pedidos pendientes:", e)  # Imprimir errores en consola
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})



def asignar_pedido(request, pedido_id):
    if request.method == 'POST':
        correo_usuario = request.session.get('correo_usuario')
        if not correo_usuario:
            return JsonResponse({'success': False, 'message': 'No estás autenticado.'})

        try:
            usuario = Usuario.objects.get(correo=correo_usuario)
            if not usuario.estado_usuario:
                return JsonResponse({'success': False, 'message': 'Debes estar activo para asignar pedidos.'})

            pedido = Pedido.objects.get(id_pedido=pedido_id, estado_pedido="pendiente")
            pedido.estado_pedido = "asignado"
            pedido.correo = usuario  # Asignar el pedido al repartidor
            pedido.save()

            return JsonResponse({'success': True, 'message': 'Pedido asignado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado.'})
        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El pedido no existe o ya fue asignado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

def marcar_no_entregado(request, pedido_id):
    if request.method == 'POST':
        try:
            pedido = Pedido.objects.get(id_pedido=pedido_id)
            pedido.estado_pedido = "no entregado"  # Cambiar el estado
            pedido.save()
            return JsonResponse({'success': True, 'message': 'El pedido ha sido marcado como "No Entregado".'})
        except Pedido.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El pedido no existe.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

