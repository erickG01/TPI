from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.utils.dateformat import DateFormat
from django.db import IntegrityError
from Negocio.models import *
from django.conf import settings
from Repartidor.models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import A4
from functools import wraps

def login_cliente(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        try:
            cliente = Cliente.objects.get(correo_cliente=email)
            if cliente.check_password(password):
                request.session['cliente_id'] = cliente.correo_cliente
              
                return redirect('menu_Diario')
            else:
                error_message = "Credenciales incorrectas"
        except Cliente.DoesNotExist:
            error_message = "Usuario no encontrado"

        return render(request, 'cliente/login_cliente.html/', {'error_message': error_message})
    return render(request, 'cliente/login_cliente.html/')

#Este metodo valida que un usuario este autentificado 
def cliente_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'cliente_id' not in request.session:
            return redirect('login_cliente')
        return view_func(request, *args, **kwargs)
    return wrapper

#Metodo para cerrar sesion
def logout_cliente(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']  
    return redirect('login_cliente')  

@cliente_login_required
def comida(request):
    productos = Producto.objects.filter(disponibilidad_producto=True)
    return render(request, 'cliente/comida.html', {'productos': productos})
   
@cliente_login_required
def reclamos(request):
    return render(request,"cliente/reclamos.html/")




@cliente_login_required
def mapa(request):
    return render(request,"cliente/mapa.html/")


def registro_cliente(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        correo_cliente = request.POST.get('correo_cliente')
        telefono_cliente = request.POST.get('telefono_cliente')
        password_cliente = request.POST.get('password_cliente')
        confirm_password_cliente = request.POST.get('confirm_password_cliente')


        if password_cliente != confirm_password_cliente:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro_cliente')
        
        if len(password_cliente) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('registro_cliente')


        try:
            cliente = Cliente.objects.create(
                nombre_cliente=nombre_cliente,
                correo_cliente=correo_cliente,
                telefono_cliente=telefono_cliente,
                password_cliente=make_password(password_cliente),
                puntos=0, 
            )
            return redirect('login_cliente')
        except IntegrityError:
           
            return redirect('registro_cliente')
        except Exception as e:
           
            return redirect('registro_cliente')

    return render(request, 'cliente/registro_cliente.html/')

@cliente_login_required
def editar_cliente(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('login_cliente')

    # Obtener el cliente
    cliente = get_object_or_404(Cliente, correo_cliente=cliente_id)

    if request.method == 'POST':
        # Actualizar los datos del cliente
        nombre = request.POST.get('nombre_cliente', '').strip()
        correo = request.POST.get('correo_cliente', '').strip()
        telefono = request.POST.get('telefono_cliente', '').strip()
        password_cliente = request.POST.get('password_cliente', '').strip()
        confirm_password_cliente = request.POST.get('confirm_password_cliente', '').strip()
        imagen_cliente = request.FILES.get('imagen_cliente')

        # Validaciones
        if password_cliente and password_cliente != confirm_password_cliente:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('editar_cliente')
        

        try:
            # Actualizar cliente
            cliente.nombre_cliente = nombre
            cliente.telefono_cliente = telefono
            cliente.correo_cliente = correo

            if password_cliente:
                cliente.password_cliente = make_password(password_cliente)

            if imagen_cliente:
                cliente.imagen_cliente = imagen_cliente

            cliente.save()

        
            return redirect('editar_cliente')

        except Exception as e:
            messages.error(request, f'Ocurrió un error al actualizar los datos: {str(e)}')
            return redirect('editar_cliente')

    return render(request, 'cliente/editar_cliente.html/', {'cliente': cliente})

@cliente_login_required
@csrf_exempt  
def gestionar_reclamos(request):
    if request.method == "POST":
        try:
            cliente_id = request.session.get('cliente_id')
            if not cliente_id:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

            cliente = Cliente.objects.get(correo_cliente=cliente_id)
            data = json.loads(request.body)
            descripcion = data.get('description')

            if not descripcion:
                return JsonResponse({'error': 'La descripción es requerida'}, status=400)

            Reclamo.objects.create(
                correo_cliente=cliente,
                descripcion_reclamo=descripcion,
                fecha_reclamo=date.today()
            )

            reclamos = Reclamo.objects.filter(correo_cliente=cliente).order_by('-id_reclamo')[:5]
            reclamos_data = [{
                'descripcion_reclamo': r.descripcion_reclamo,
                'fecha_reclamo': DateFormat(r.fecha_reclamo).format('d/m/Y')
            } for r in reversed(reclamos)]

            return JsonResponse({'reclamos': reclamos_data}, status=200)

        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    elif request.method == "GET":
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

        try:
            cliente = Cliente.objects.get(correo_cliente=cliente_id)
            reclamos = Reclamo.objects.filter(correo_cliente=cliente).order_by('-id_reclamo')[:5]
            reclamos_data = [{
                'descripcion_reclamo': r.descripcion_reclamo,
                'fecha_reclamo': DateFormat(r.fecha_reclamo).format('d/m/Y')
            } for r in reversed(reclamos)]
            return JsonResponse({'reclamos': reclamos_data}, status=200)

        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@cliente_login_required
def crear_direccion(request):
    if request.method == "POST":
        # Recuperar al cliente actual desde la sesión
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            messages.error(request, "Debe iniciar sesión para agregar una dirección.")
            return redirect('login_cliente')

        try:
            cliente = Cliente.objects.get(correo_cliente=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, "Cliente no encontrado.")
            return redirect('login_cliente')

        nombre = request.POST['nombre']
        departamento = request.POST['departamento']
        numero_casa = request.POST['numero_casa']
        municipio = request.POST['municipio']
        calle = request.POST['calle']
        punto_referencia = request.POST['punto_referencia']

        Direccion.objects.create(
            cliente=cliente,
            nombre_direccion=nombre,
            departamento=departamento,
            numero_casa=numero_casa,
            municipio=municipio,
            calle=calle,
            punto_referencia=punto_referencia,
        )

        return redirect('direcciones') 

    return render(request, 'cliente/crear_direccion.html/')

@cliente_login_required
def editar_direccion(request, id_direccion):
 
    direccion = get_object_or_404(Direccion, id_direccion=id_direccion)
    
    if request.method == 'POST':
        # Actualizar datos con los valores enviados en el formulario
        direccion.nombre_direccion = request.POST.get('nombre', direccion.nombre_direccion)
        direccion.numero_casa = request.POST.get('numero_casa', direccion.numero_casa)
        direccion.calle = request.POST.get('calle', direccion.calle)
        direccion.punto_referencia = request.POST.get('punto_referencia', direccion.punto_referencia)
        
    
        direccion.departamento = request.POST.get('departamento', direccion.departamento)
        direccion.municipio = request.POST.get('municipio', direccion.municipio)
        
        direccion.save()
        return redirect('direcciones')  
    
    return render(request, 'cliente/editar_direccion.html/', {'direccion': direccion})

@cliente_login_required
def obtener_direcciones(request):
    # Verifica si el cliente está logueado consultando la sesión
    cliente_email = request.session.get('cliente_id')
    if not cliente_email:  # Si no hay cliente logueado, retorna error
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    try:
        # Busca al cliente utilizando el correo almacenado en la sesión
        cliente = Cliente.objects.get(correo_cliente=cliente_email)
        # Filtra las direcciones asociadas al cliente
        direcciones = Direccion.objects.filter(cliente=cliente)
        # Construye una lista de diccionarios con los datos de las direcciones
        data = [
            {
                'id_direccion': direccion.id_direccion,
                'nombre_direccion': direccion.nombre_direccion,
                'calle': direccion.calle,
                'numero_casa': direccion.numero_casa,
                'municipio': direccion.municipio,
                'departamento': direccion.departamento,
                'punto_referencia': direccion.punto_referencia,
            }
            for direccion in direcciones
        ]
        return JsonResponse(data, safe=False)  # Retorna el JSON con las direcciones
    except Cliente.DoesNotExist:  # Si el cliente no existe, redirige al login
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

@cliente_login_required
def eliminar_direccion(request, id_direccion):

    direccion = get_object_or_404(Direccion, pk=id_direccion)

    if request.method == "POST": 
        direccion.delete()
        return redirect('direcciones') 

    return redirect('direcciones') 

   
@cliente_login_required
def mostrar_direcciones(request):
    # Obtener el correo del cliente logueado desde la sesión
    cliente_email = request.session.get('cliente_id')

    # Obtener el cliente correspondiente al correo
    try:
        cliente = Cliente.objects.get(correo_cliente=cliente_email)
        direcciones = Direccion.objects.filter(cliente=cliente)
    except Cliente.DoesNotExist: 
        return redirect('login_cliente')
    
    return render(request, 'cliente/direcciones.html/', {'direcciones': direcciones})

@cliente_login_required
def menu_diario(request):
    # Obtener los detalles del menú relacionados con los productos
    detalles_menu = Detalle_Menu.objects.select_related('id_producto').values(
        'id_producto',  # ID del producto
        'id_producto__imagen_producto',  # URL de la imagen del producto
        'id_producto__nombre_producto',  # Nombre del producto
        'id_producto__precio_producto',  # Precio del producto
        'id_producto__descripcion_producto'  # Descripción del producto
    )
    
    # Procesar cada detalle para asegurar que la URL de la imagen sea válida
    for detalle in detalles_menu:
        # Generar una URL válida para la imagen
        if detalle['id_producto__imagen_producto']:
            detalle['imagen_url'] = f"{settings.MEDIA_URL}{detalle['id_producto__imagen_producto']}"
        else:
            # Asignar una imagen por defecto si no hay una imagen disponible
            detalle['imagen_url'] = f"{settings.MEDIA_URL}productos/producto_defecto.png"

    # Renderizar la plantilla con los detalles del menú
    return render(request, 'cliente/menu_Diario.html', {'detalles_menu': detalles_menu})

#vista del carrito
@cliente_login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    
    # Limpiar productos inválidos del carrito
    carrito = {k: v for k, v in carrito.items() if 'precio' in v and 'cantidad' in v}
    request.session['carrito'] = carrito
    request.session.modified = True

    total = sum(
        item.get('precio', 0) * item.get('cantidad', 1)
        for item in carrito.values()
    )

    for item in carrito.values():
        item['subtotal'] = item.get('precio', 0) * item.get('cantidad', 1)

    return render(request, 'cliente/carrito_cliente.html/', {'carrito': carrito, 'total': total})



# Vista para agregar productos al carrito
@cliente_login_required
def agregar_al_carrito(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)

    # Inicializa el carrito en la sesión si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = {}

    carrito = request.session['carrito']

    # Si el producto ya está en el carrito, incrementa la cantidad
    if str(id_producto) in carrito:
        carrito[str(id_producto)]['cantidad'] += 1
    else:
       carrito[str(id_producto)] = {
       'nombre': producto.nombre_producto,
       'precio': float(producto.precio_producto) if producto.precio_producto else 0.0,  # Asegura un  precio válido
       'cantidad': 1,
       'imagen': producto.imagen_producto.url if producto.imagen_producto else None,
       'id': producto.id_producto
    }

    request.session.modified = True  
    return redirect('ver_carrito')

# Vista para eliminar un producto del carrito
@cliente_login_required
def eliminar_del_carrito(request, id_producto=None):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if id_producto:
            # Eliminar un producto específico
            if str(id_producto) in carrito: 
                del carrito[str(id_producto)]
                messages.success(request, "Producto eliminado del carrito.")
            else:
                messages.error(request, "El producto no está en el carrito.")
        else:
            # Vaciar todo el carrito
            carrito.clear()
            messages.success(request, "Carrito vaciado correctamente.")

        request.session['carrito'] = carrito
        request.session.modified = True
    else:
        messages.error(request, "El carrito ya está vacío.")

    return redirect('ver_carrito')


#actualiza cantidad
@cliente_login_required
def actualizar_carrito(request, id_producto, nueva_cantidad):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if str(id_producto) in carrito and nueva_cantidad > 0:
            carrito[str(id_producto)]['cantidad'] = nueva_cantidad
            request.session.modified = True
            messages.success(request, "Cantidad actualizada.")
        else:
            messages.error(request, "Cantidad no válida.")

    return redirect('ver_carrito')

@cliente_login_required
def registrar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            metodo_pago = data.get('metodoPago')
            id_direccion = data.get('direccionSeleccionada') 
            total_pago = data.get('total')  
            ids_productos = data.get('ids')
            cantidad = data.get('cantidad')
            if total_pago is None:
                return JsonResponse({'error': 'Total no recibido'}, status=400)
            
            #Convierte el total_pago a Decimal
            total_pago = Decimal(str(total_pago))

      
            if not metodo_pago or not id_direccion:
                return JsonResponse({'error': 'Datos incompletos'}, status=400)

            try:
                direccion = Direccion.objects.get(id_direccion=id_direccion)
            except Direccion.DoesNotExist:
                return JsonResponse({'error': 'Dirección no encontrada'}, status=404)
            cliente = direccion.cliente
            correo_cliente = cliente.correo_cliente  

            try:
                usuario = Usuario.objects.get(correo="admin@admin.com")
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            
            pago = Pago.objects.create(
                correo_cliente=cliente,  
                total_pago=total_pago,         
                tipo_pago=metodo_pago,      
            )

            # Crear el pedido
            pedido = Pedido.objects.create(
                correo=usuario,             
                id_direccion=direccion,     
                id_pago=pago,             
                estado_pedido="Pendiente",  
            )

            for ids,cantidad_producto in zip(ids_productos,cantidad):
                producto = Producto.objects.get(id_producto = ids)
                detalle = Detalle_Producto(
                    id_producto = producto,
                    id_pedido = pedido,
                    cantidad_detalle = cantidad_producto
                )
                detalle.save()
                

            # Retornar respuesta exitosa
            return JsonResponse({
                'mensaje': 'Pedido registrado exitosamente',
                'pedido_id': pedido.id_pedido  # Devolver el ID del pedido
            }, status=201)

        except Exception as e:
            # Capturar cualquier otro error y devolverlo
            return JsonResponse({'error': str(e)}, status=500)

    # Si no es un POST, redirigir al carrito
    return redirect('ver_carrito')

# Vista para mostrar los productos en la página de comida
@cliente_login_required
def productos(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'default_image': '/static/productos/producto_defecto.png', 
    }
    return render(request, 'cliente/comida.html/', context)


def manifest(request):
    path = request.path  # Esto debería siempre ser /manifest.json
    
    
    # Determina el manifiesto según el contexto (puedes usar sesiones, subdominios, etc.)
    if '/repartidor' in request.META.get('HTTP_REFERER', ''):
        manifest = {
            "name": "Repartidor",
            "short_name": "Repartidor",
            "description": "Aplicación para repartidores del restaurante",
            "theme_color": "#1E88E5",
            "background_color": "#FFFFFF",
            "display": "standalone",
            "scope": "/repartidor/",
            "start_url": "/repartidor/login",
            "orientation": "portrait",
            "status_bar": "default",
            "icons": [
                {
                    "src": "/static/imagenes/Repartidor/app-icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                     "purpose": "any",
                }
            ],
            "screenshots": [
                {
                    "src": "/static/imagenes/screenshots/screenshot3.png",
                    "sizes": "508x808",
                    "type": "image/png",
                    "form_factor": "wide"
                }
            ],
            "dir": "ltr",
            "lang": "es-MX"
        }
    else:
        manifest = {
            "name": "Cliente",
            "short_name": "Cliente",
            "description": "Aplicación para clientes del restaurante",
            "theme_color": "#000000",
            "background_color": "#9d0b74",
            "display": "standalone",
            "scope": "/",
            "start_url": "/clientes/",
            "orientation": "portrait",
            "status_bar": "default",
            "icons": [
                {
                    "src": "/static/imagenes/icons/app-icon-144x144.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any"
                },
                 {
                    "src": "/static/imagenes/icons/app-icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ],
            "screenshots": [
                {
                    "src": "/static/imagenes/screenshots/screenshot1.png",
                    "sizes": "1915x1078",
                    "type": "image/png",
                    "form_factor": "narrow"
                },
                {
                    "src": "/static/imagenes/screenshots/screenshot2.jpeg",
                    "sizes": "488x1055",
                    "type": "image/png",
                    "form_factor": "wide"
                }
            ],
            "dir": "ltr",
            "lang": "es-MX"
        }

  
    return JsonResponse(manifest)


#Descuento por cupones
@cliente_login_required
@login_required
def cupones_cliente(request):
    # Verifica si el cliente está logueado consultando la sesión
    cliente_email = request.session.get('cliente_id')
    if not cliente_email:  # Si no hay cliente logueado, retorna error
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
    
    try:
        # Busca al cliente utilizando el correo almacenado en la sesión
        cliente = Cliente.objects.get(correo_cliente=cliente_email)
        # Filtra los descuentos asociadas al cliente
        descuentos = Descuento.objects.filter(correo_cliente=cliente)
        # Construye una lista de diccionarios con los datos de las direcciones
        data = [
            {
                'id_descuento': descuento.id_descuento,
                'tipo_descuento': descuento.tipo_descuento,
                'monto_descuento': descuento.monto_descuento,
                'estado_descuento': descuento.estado_descuento,
                'fecha_vencimiento': descuento.fecha_vencimiento,
            }
            for descuento in descuentos
        ]
        return JsonResponse(data, safe=False)  # Retorna el JSON con las direcciones
    except Cliente.DoesNotExist:  # Si el cliente no existe, redirige al login
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

#eliminar_descuento
def eliminar_descuento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
            print("Datos recibidos:", data)  # Imprime los datos para depurar

            id_descuento = data.get('id_descuento')  # Obtén el ID del descuento
            print("datos", id_descuento)
            if not id_descuento:
                return JsonResponse({'error': 'ID de descuento no proporcionado'}, status=400)
            
            # Buscar y eliminar el descuento
            descuento = Descuento.objects.filter(id_descuento=id_descuento).first()  

            if not descuento:
                return JsonResponse({'error': 'Descuento no encontrado', 'id_descuento': id_descuento}, status=404)

            descuento.delete()

            return JsonResponse({'mensaje': 'Descuento eliminado exitosamente'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar la solicitud'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

#factura
def generar_factura(request):
    carrito = request.session.get('carrito', {})

    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    cliente = get_object_or_404(Cliente, correo_cliente=request.user.email)

    nombre_cliente = cliente.nombre_cliente 

    # Obtener el descuento si existe
    descuento = Descuento.objects.filter(correo_cliente=cliente, estado_descuento=True).first()
    monto_descuento = descuento.monto_descuento if descuento else 0

    # Obtener el método de pago
    pago = Pago.objects.filter(correo_cliente=cliente).first()
    metodo_pago = pago.tipo_pago if pago else "No especificado"

    # Obtener el pedido relacionado (último pedido del cliente)
    pedido = Pedido.objects.filter(correo=cliente.correo_cliente).last()
    detalles_pedido = Detalle_Producto.objects.filter(id_pedido=pedido) if pedido else []

    # Calcular el total
    total = subtotal - float(monto_descuento)

    context = {
        'carrito': carrito,
        'subtotal': subtotal,
        'monto_descuento': monto_descuento,
        'total': total,
        'metodo_pago': metodo_pago,
        'pedido': pedido,
        'detalles_pedido': detalles_pedido,
        'nombre_cliente': nombre_cliente,  # Agregar el nombre del cliente al contexto
    }

    # Generar el PDF
    html_string = render_to_string('cliente/factura_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="factura.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)

    return response
