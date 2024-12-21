from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from Negocio.models import *
from Cliente.models import Cliente
from Repartidor.models import *
from decimal import Decimal
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from utils import *
from django.http import JsonResponse
from .models import Producto
from Cliente.models import *
import json
import os
from django.core.files.storage import default_storage
from pathlib import Path



# Create your views here.
def Login(request):
    color_scheme = get_color_scheme()
    return render(request,'negocio/login.html',{"color_scheme":color_scheme})

#Recuperar Clave
def recuperarClave(request):
    return render(request,'negocio/recuperar_password.html')

def vistaRestablecer(request):
    return render(request,'negocio/restablecer.html')

#Enviar Correo
def EnviarCorreo(request):
    correo_destinatario = request.POST.get('email')
    if correo_destinatario:

        exite = Usuario.objects.filter(correo = correo_destinatario).exists()
        if exite:
            asunto = 'Recuperación de Contraseña'
            enlace_recuperacion = 'http://127.0.0.1:8000/negocio/restablecer'
            mensaje = render_to_string('negocio/recuperacion.html',{'enlace_recuperacion':enlace_recuperacion})
            correo_remitente = settings.DEFAULT_FROM_EMAIL

            email = EmailMessage(
                asunto,
                mensaje,
                correo_remitente,
                [correo_destinatario],
            )

            email.content_subtype = 'html'
            email.send()

            messages.success(request,'Correo Enviado')
            return redirect('login_negocio')
        else:
            messages.error(request,'Usuario No Encontrado')
            return redirect('recuperar_negocio_clave')

def ActualizarPerfil(request):
    color_scheme = get_color_scheme()
    correo = request.session.get('correo_usuario','Correo no identificado')

    if 'correo_usuario' in request.session:
        try:
            usuario = Usuario.objects.get(correo=correo)
            if(usuario.rol_usuario == 'Administrador'):
                template = 'negocio/menuAdministrador.html'
            elif (usuario.rol_usuario == 'Administrador Menú'):
                template = 'negocio/producto/menuAdminMenu.html'
            elif (usuario.rol_usuario == 'Administrador Despacho'):
                template = 'negocio/menuDespachoPedidos.html'
            return render(request,'negocio/actualizarPerfil.html',{
                "color_scheme":color_scheme,
                "usuario":usuario,
                'template': template
            })
        except Usuario.DoesNotExist:
            messages.error(request,"Usuario No Encontrado")
            return('negocio/perfil')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def ActualizarUsuario(request):
    correo = request.session.get('correo_usuario','Correo no identificado')

    if 'correo_usuario' in request.session:
        nombre = request.POST.get('nombre_usuario')
        password = request.POST.get('password_usuario')
        imagen = request.FILES.get('imagen')

        
        try:
            user = Usuario.objects.get(correo = correo)
            if imagen:
                if user.imagen and user.imagen.name != 'usuarios/usuario_defecto.png':
                    default_storage.delete(user.imagen.name)
                
                user.nombre_usuario = nombre
                user.password_usuario = password
                user.imagen = imagen
                user.save()
                return redirect('negocio_perfil')
            else:
                user.nombre_usuario = nombre
                user.password_usuario = password
                user.save()
                return redirect('negocio_perfil')
        except Usuario.DoesNotExist:
            messages.error(request,'No se puedo actualizar la informacion')
            return redirect('actualizar_perfil')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def Perfil_Usuario(request):
    correo = request.session.get('correo_usuario','Correo no identificado')
    color_scheme = get_color_scheme()
    
    if 'correo_usuario' in request.session:

        try:
            usuario = Usuario.objects.get(correo=correo)
            if(usuario.rol_usuario == 'Administrador'):
                template = 'negocio/menuAdministrador.html'
            elif (usuario.rol_usuario == 'Administrador Menú'):
                template = 'negocio/producto/menuAdminMenu.html'
            elif (usuario.rol_usuario == 'Administrador Despacho'):
                template = 'negocio/menuDespachoPedidos.html'

            return render(request,'negocio/perfil.html',{
                "color_scheme":color_scheme,
                "usuario":usuario,
                'template': template
            })
        except Usuario.DoesNotExist:
            messages.error(request,"Usuario No Encontrado")
            return('negocio/perfil')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def IniciarSesion(request):
    correo = request.POST.get('txtCorreo')
    password = request.POST.get('txtPassword')

    try:
        usuario = Usuario.objects.get(correo = correo,password_usuario = password)
        if usuario:
            request.session['correo_usuario'] = usuario.correo
            usuario.estado_usuario = True
            usuario.save()
            if usuario.rol_usuario == 'Administrador':
                return redirect('inicio_negocio_administrador')
            if usuario.rol_usuario == 'Administrador Menú':
                return redirect('inicio_negocio_menu')
            if usuario.rol_usuario == 'Administrador Repartidor':
                return redirect('login_repartidor')
            if usuario.rol_usuario == 'Administrador Despacho':
                return redirect('inicio_despacho')
    except Usuario.DoesNotExist:
        messages.error(request,'Correo o contraseña incorrectos. Inténte de nuevo.')
        return redirect('login_negocio')
    
def CerrarSesionNegocio(request):
    try:
        usuario = Usuario.objects.get(correo = request.session['correo_usuario'])
        usuario.estado_usuario = False
        usuario.save()
        del request.session['correo_usuario']
        del request.session['nombre_usuario']
        del request.session['rol_usuario']
    except KeyError:
        pass
    return redirect('login_negocio')

def InicioAdministrador(request):
    correo = request.session.get('correo_usuario','Correo no identificado')
    color_scheme = get_color_scheme()

    #ruta al json
    config_file = Path(__file__).resolve().parent.parent / 'config' / 'configuracion_empresa.json'

    with open(config_file,'r', encoding='utf-8') as file:
        empresa_config = json.load(file)
    if 'correo_usuario' in request.session:

        try:
            usuario = Usuario.objects.get(correo = correo)
            return render(request,'negocio/administrador.html',{
                "color_scheme":color_scheme,
                'usuario':usuario,
                'empresa':empresa_config
             })
        except Usuario.DoesNotExist:
            return redirect('login_negocio')
    else: 
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def Registrar(request,gestion):
    color_scheme = get_color_scheme()
    
    
    #ruta al json
    config_file = Path(__file__).resolve().parent.parent / 'config' / 'configuracion_empresa.json'

    with open(config_file,'r', encoding='utf-8') as file:
        empresa_config = json.load(file)

    if 'correo_usuario' in request.session:
        return render(request,'negocio/registrar.html',{"color_scheme":color_scheme,"gestion":gestion,'empresa':empresa_config})
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

#Funciones para Administrar el Menu
def ActualizarColoresMenu(request):
    color_scheme = get_color_scheme()
    if 'correo_usuario' in request.session:
        return render(request,'negocio/menu.html',{"color_scheme":color_scheme})
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def InicioMenu(request):
    color_scheme = get_color_scheme()
    correo = request.session.get('correo_usuario','Correo no identificado')
    if 'correo_usuario' in request.session:
        template = 'negocio/producto/menuAdminMenu.html'
        try:
            usuario = Usuario.objects.get(correo = correo)
            return render(request,'negocio/producto/menu.html',{"color_scheme":color_scheme,'template':template,'usuario':usuario})
        except Usuario.DoesNotExist:
            return redirect('login_negocio')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')


def inicioProductos(request):
    color_scheme = get_color_scheme()
    if 'correo_usuario' in request.session:
        productos = Producto.objects.all()
        return render(request,'negocio/producto/index.html',{
            "color_scheme":color_scheme,
            "productos":productos
            })
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def crearProducto(request):
    if 'correo_usuario' in request.session:

        nombre_producto = request.POST.get('nombre_producto')
        precio_producto = request.POST.get('precio_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        disponibilidad_producto = request.POST.get('disponibilidad_producto')
        imagen_producto = request.FILES.get('imagen_producto')

        correo = request.session.get('correo_usuario','Correo no identificado')
        try:

            try:
                usuario = Usuario.objects.get(correo=correo)
            except Usuario.DoesNotExist:
                pass
            datos_producto = {
                'correo': usuario,
                'nombre_producto': nombre_producto,
                'precio_producto': precio_producto,
                'disponibilidad_producto': disponibilidad_producto,
                'descripcion_producto': descripcion_producto,
            }
            if imagen_producto:
                datos_producto['imagen_producto'] = imagen_producto

            producto = Producto(**datos_producto)
            producto.save()
            return redirect('inicio_producto')
        except IntegrityError:
            return redirect('inicio_producto')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

    
def actualizarProducto(request):
    if 'correo_usuario' in request.session:
        id_producto = request.POST.get('producto_id')
        nombre_producto = request.POST.get('nombre_producto')
        descripcion_producto = request.POST.get('descripcion_producto')
        disponibilidad_producto = request.POST.get('disponibilidad_producto')
        imagen_producto = request.FILES.get('imagen_producto')

        try: 
            precio_producto = Decimal(request.POST.get('precio_producto'))
            try:
                correo = request.session.get('correo_usuario','Correo no identificado')
                usuario = Usuario.objects.get(correo=correo)
            except Usuario.DoesNotExist:
                pass
            try:
                producto = Producto.objects.get(id_producto = id_producto)
                producto.correo = usuario
                producto.nombre_producto = nombre_producto
                producto.precio_producto = precio_producto
                producto.disponibilidad_producto = disponibilidad_producto
                producto.descripcion_producto = descripcion_producto
                if imagen_producto:
                    if producto.imagen_producto and producto.imagen_producto.name != 'productos/producto_defecto.png':
                        default_storage.delete(producto.imagen_producto.name)
                    producto.imagen_producto = imagen_producto

                producto.save()
                return redirect('inicio_producto')
            except Producto.DoesNotExist:
                messages.error(request,'!Error!, Producto no existente')
                return redirect('inicio_producto')
        except (ValueError,TypeError):
            precio_producto = Decimal(0)
            messages.error(request,'!Error!, Valor Erroneo')
            return redirect('inicio_producto')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')
    
def crearMenu(request):
    if 'correo_usuario' in request.session:
        color_scheme = get_color_scheme()
        productos = Producto.objects.all().filter(disponibilidad_producto = True)
        return render(request,'negocio/producto/crearMenu.html',{"color_scheme":color_scheme,'productos':productos})
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def CrearMenu_DetalleMenu(request):
    if 'correo_usuario' in request.session:

        fecha = request.POST.get('fecha_menu')
        productos_ids = request.POST.getlist('productos_seleccionados')

        correo = request.session.get('correo_usuario','Correo no identificado')

        if productos_ids and isinstance(productos_ids[0],str):
            ids = [int(id_producto) for id_producto in productos_ids[0].split(',')]
        else:
            ids = []
        try:
            usuario = Usuario.objects.get(correo = correo)
            try:
                menu = Menu(
                    correo = usuario,
                    fecha_menu = fecha
                )
                menu.save()
                for producto in ids:
                    try:
                        id_poducto = Producto.objects.get(id_producto = producto)
                    except Producto.DoesNotExist:
                        messages.error(request,'Producto No Encontrado')
                    try:
                        detalle = Detalle_Menu(
                            id_menu = menu,
                            id_producto = id_poducto
                        )
                        detalle.save()
                    except IntegrityError:
                        messages.error(request,'Detalle No Creado')
            except IntegrityError:
                messages.error(request,'Menu No Creado')
        except Usuario.DoesNotExist:
            messages.error(request,'Error al buscar el usuario')

        return redirect('crear_menu')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def MenusDisponibles(request):
    if 'correo_usuario' in request.session:

        color_scheme = get_color_scheme()
        menu = Menu.objects.all().values()
        return render(request,'negocio/producto/menusDisponibles.html',{
            "color_scheme":color_scheme,
            'menus': menu,
            })
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def filtarMenuDetalle(request):
    if 'correo_usuario' in request.session:
        detalles = Detalle_Menu.objects.values()
        productos = Producto.objects.values()
        return JsonResponse({
            'detalle':list(detalles),
            'productos':list(productos)
            },safe=False)
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def EliminarMenu(request):
    if 'correo_usuario' in request.session:

        id_menu = request.POST.get('menu_id')
        try:
            detalle_menu = Detalle_Menu.objects.filter(id_menu_id = id_menu)
            detalle_menu.delete()
            menu = Menu.objects.get(id_menu = id_menu)
            menu.delete()
            return redirect('menus_disponibles')
        except Exception as e:
            messages.error(request,'Error al eliminar el menu')
            return redirect('menus_disponibles')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def gestionarUsuarios(request,gestion):
    if 'correo_usuario' in request.session:
        color_scheme = get_color_scheme()
        return render(request,'negocio/gestionarUsuario.html',{
            "color_scheme":color_scheme,
            "gestion":gestion
        })
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def actualizarUsuario(request, gestion):
    if 'correo_usuario' in request.session:
        color_scheme = get_color_scheme()
        correo = request.POST.get('email')
        usuario = None

        roles_permitidos = {
            'Administracion': 'Administrador',
            'Menú': 'Administrador Menú',
            'Pedidos': 'Administrador Pedidos',
            'Despacho': 'Administrador Despacho',
            'Repartidores': 'Administrador Repartidor'
        }

        if correo:
            try:
                user = Usuario.objects.get(correo=correo)
                if user.rol_usuario == roles_permitidos.get(gestion):
                    usuario = user
                else:
                    messages.error(request, 'El usuario no pertenece a esta gestión.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no existe.')

        return render(request, 'negocio/actualizarUsuario.html', {
            "color_scheme": color_scheme,
            "gestion": gestion,
            "usuario": usuario
        })
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def editarUsuario(request,gestion):
    if 'correo_usuario' in request.session:

        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre_usuario')
        password = request.POST.get('password_usuario')
        imagen = request.FILES.get('imagen')

        try:
            usuario = Usuario.objects.get(correo = correo)
            if imagen:
                usuario.imagen = imagen
            if nombre and password:
                usuario.nombre_usuario = nombre
                usuario.password_usuario = password
            elif nombre:
                usuario.nombre_usuario = nombre
            elif password:
                usuario.password_usuario = password
            usuario.save()
            messages.success(request,'Usuario Actualizado con Exito')
            return redirect('actualizarUsuario',gestion)
        except Usuario.DoesNotExist:
            messages.error(request,'No se puedo hacer la actualizacion')
            return redirect('actualizarUsuario',gestion)
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def BuscarUsuario(request, gestion):

    if 'correo_usuario' in request.session:

        color_scheme = get_color_scheme()
        correo = request.POST.get('email')
        usuario = None

        roles_permitidos = {
            'Administracion': 'Administrador',
            'Menú': 'Administrador Menú',
            'Pedidos': 'Administrador Pedidos',
            'Despacho': 'Administrador Despacho',
            'Repartidores': 'Administrador Repartidor'
        }

        if correo:
            try:
                user = Usuario.objects.get(correo=correo)
                if user.rol_usuario == roles_permitidos.get(gestion):
                    usuario = user
                else:
                    messages.error(request, 'El usuario no pertenece a esta gestión.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no existe.')

        return render(request, 'negocio/buscarUsuario.html', {
            "color_scheme": color_scheme,
            "gestion": gestion,
            "usuario": usuario
        })
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')



def crearUsuario(request):

    if 'correo_usuario' in request.session:

        correo = request.POST.get('txtCorreoNuevo')
        nombre = request.POST.get('txtNombreUsuario')
        password = request.POST.get('txtPassword')
        imagen = request.FILES.get('profile_image')
        rol = request.POST.get('rol')
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request,'Ya existe un usuario registrado con este correo: '+correo)
            return redirect('registrar_usuario',rol)
        
        roles = {
            'Administracion': 'Administrador',
            'Menú': 'Administrador Menú',
            'Pedidos': 'Administrador Pedidos',
            'Despacho': 'Administrador Despacho',
            'Repartidores': 'Administrador Repartidor'
        }

        try:
            if rol in roles:
                datos_usuario = {
                    'correo': correo,
                    'nombre_usuario': nombre,
                    'rol_usuario': roles[rol],
                    'password_usuario': password,
                    'estado_usuario': False,
                }
                if imagen:
                    datos_usuario['imagen'] = imagen
                
                usuario = Usuario(**datos_usuario)
                usuario.save()
                messages.success(request,'Usuario Registrado Con Exito')
                return redirect('registrar_usuario',rol)
            else:
                messages.error(request,'Rol no válido')
                return redirect('registrar_usuario',rol)
        except IntegrityError:
            messages.error(request,'El Usuario: '+correo+'. Ya esta registrado')
            return redirect('registrar_usuario',rol)
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def Menu_Detalle_Menu(request):
    if 'correo_usuario' in request.session:

        menu = list(Menu.objects.all().values())
        detalle_Menu = list(Detalle_Menu.objects.all().values())
        return JsonResponse({"menu": menu,"detalle_menu":detalle_Menu}, safe=False)
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def Preferencias(request):

    if 'correo_usuario' in request.session:

        color_scheme = get_color_scheme()
        # obtener el Usuario que esta logeado
        correo = request.session.get('correo_usuario','Correo no identificado')
        try:
            usuario = Usuario.objects.get(correo=correo)
            if(usuario.rol_usuario == 'Administrador'):
                template = 'negocio/menuAdministrador.html'
            elif (usuario.rol_usuario == 'Administrador Menú'):
                template = 'negocio/producto/menuAdminMenu.html'
            elif (usuario.rol_usuario == 'Administrador Despacho'):
                template = 'negocio/menuDespachoPedidos.html'
            return render(request,'negocio/preferencias.html',{"color_scheme":color_scheme,"user":usuario ,"template":template})
        except Usuario.DoesNotExist:
            messages.error(request,'Usuario No Encontrado')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')


def Soporte(request):

    if 'correo_usuario' in request.session:
        color_scheme = get_color_scheme()
        correo = request.session.get('correo_usuario','Correo no identificado')
        try:
            usuario = Usuario.objects.get(correo=correo)
            if(usuario.rol_usuario == 'Administrador'):
                template = 'negocio/menuAdministrador.html'
            elif (usuario.rol_usuario == 'Administrador Menú'):
                template = 'negocio/producto/menuAdminMenu.html'
            elif (usuario.rol_usuario == 'Administrador Despacho'):
                template = 'negocio/menuDespachoPedidos.html'
            return render(request,'negocio/soporte.html',{"color_scheme":color_scheme,"user":usuario ,"template":template})
        except Usuario.DoesNotExist:
            messages.error(request,'Usuario No Encontrado')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

def cambiarColores(request):

    if 'correo_usuario' in request.session:

        color_scheme = {
            "color_primario": request.POST.get("color_primario", "bg-dark"),
            "color_texto_primario": request.POST.get("color_texto_primario", "bg-light"),
            "color_secundario": request.POST.get("color_secundario", "text-white"),
            "color_texto_secundario": request.POST.get("color_texto_secundario", "text-dark"),
        }
        with open(settings.COLOR_FILE, 'w') as file:
                json.dump(color_scheme, file)
        return redirect('inicio_negocio_administrador')
    else:
        messages.error(request,'! Inicia Sesion Primero Para Acceder !')
        return redirect('login_negocio')

#Lealtad
def gestionarLealtad(request):
    color_scheme = get_color_scheme()
    
    programa_lealtad_activo = request.session.get('programa_lealtad_activo', True) 
    # Lógica para activar o desactivar el programa de lealtad
    if request.method == 'POST':
        if 'activar_programa' in request.POST:
            request.session['programa_lealtad_activo'] = True
            programa_lealtad_activo = True
            Descuento.objects.filter(tipo_descuento='Puntos').update(estado_descuento=True)
            messages.warning(request, "El programa de lealtad ha sido activado y todos los puntos han sido marcados como activos.") 
        elif 'desactivar_programa' in request.POST:
            request.session['programa_lealtad_activo'] = False
            programa_lealtad_activo = False  
            Descuento.objects.filter(tipo_descuento='Puntos').update(estado_descuento=False)
            messages.warning(request, "El programa de lealtad ha sido desactivado y todos los puntos han sido marcados como inactivos.")


    search_email = request.GET.get('search_email')
    search_email = request.GET.get('search_email')
    if search_email:
        cupones = Descuento.objects.filter(correo_cliente=search_email, tipo_descuento='Cupón')
        puntos = Descuento.objects.filter(correo_cliente=search_email, tipo_descuento='Puntos')
    else:
        cupones = Descuento.objects.filter(tipo_descuento='Cupón')
        puntos = Descuento.objects.filter(tipo_descuento='Puntos')

    # CUPON
    #Creación del cupon
    if request.method == 'POST' and 'create_cupon' in request.POST:
        #id_descuento = request.POST.get('id_descuento')
        correo = request.session.get('correo_usuario','Correo no identificado')
        correo_cliente = request.POST.get('correo_cliente')
        tipo_descuento = request.POST.get('tipo_descuento')
        monto_descuento = request.POST.get('monto_descuento')
        estado_descuento = request.POST.get('estado_descuento') == 'True'
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        try:
            admin = Usuario.objects.get(correo = correo)
            try:
                cliente = Cliente.objects.get(correo_cliente = correo_cliente)
            except Cliente.DoesNotExist:
                messages.error(request,'Error, el cliente no existe')
                return redirect('gestionarLealtad') 
            des = Descuento(
                correo=admin,
                correo_cliente=cliente,  
                tipo_descuento=tipo_descuento,
                monto_descuento=monto_descuento,
                estado_descuento=estado_descuento,
                fecha_vencimiento=fecha_vencimiento,
            )
            des.save()
            messages.success(request, "El cupón ha sido creado correctamente.")
            return redirect('gestionarLealtad') 
        except Usuario.DoesNotExist:
            messages.error(request,'Error, Usuario No Existe')
            return redirect('gestionarLealtad') 

    # Edicion del cupon
    if request.method == 'POST' and 'edit_cupon' in request.POST:
        id_descuento_actualizar = request.POST.get('id_descuento_actualizar')
        monto_descuento_actualizar = request.POST.get('monto_descuento_actualizar')
        estado_descuento_actualizar = request.POST.get('estado_descuento_actualizar') == 'True'
        fecha_vencimiento_actualizar = request.POST.get('fecha_vencimiento_actualizado')

        try:
            descuento_actualizar = Descuento.objects.get(id_descuento = id_descuento_actualizar)
            descuento_actualizar.monto_descuento = monto_descuento_actualizar
            descuento_actualizar.estado_descuento = estado_descuento_actualizar
            descuento_actualizar.fecha_vencimiento = fecha_vencimiento_actualizar
            descuento_actualizar.save()
            messages.success(request, "El cupón ha sido Actualizado correctamente.")
            return redirect('gestionarLealtad')
        except IntegrityError as e:
            messages.error(request, "Ocurrio Error: "+ str(e))
            return redirect('gestionarLealtad')

    # Eliminación del cupon
    if request.method == 'POST' and 'delete' in request.POST:
        id_descuento = request.POST.get('id_descuento')
        descuento = Descuento.objects.get(id_descuento = id_descuento)
        descuento.delete()
        messages.success(request, "El cupón ha sido eliminado correctamente.")
        return redirect('gestionarLealtad')
    
    #PUNTOS
    #Creación de puntos
    if request.method == 'POST' and 'create_puntos' in request.POST:
        if not programa_lealtad_activo:
            messages.warning(request, "No se pueden crear puntos porque el programa de lealtad está desactivado.")
            return redirect('gestionarLealtad') 
        else: 
            #id_descuento = request.POST.get('id_descuento')
            correo = request.session.get('correo_usuario','Correo no identificado')
            correo_cliente = request.POST.get('correo_cliente')
            tipo_descuento = request.POST.get('tipo_descuento')
            monto_descuento = request.POST.get('monto_descuento')
            estado_descuento = request.POST.get('estado_descuento') == 'True'
            fecha_vencimiento = request.POST.get('fecha_vencimiento')

        try:
            admin = Usuario.objects.get(correo = correo)
            try:
                cliente = Cliente.objects.get(correo_cliente = correo_cliente)
            except Cliente.DoesNotExist:
                messages.error(request,'Error, el cliente no existe')
                return redirect('gestionarLealtad') 
            pun = Descuento(
                correo=admin,
                correo_cliente=cliente,  
                tipo_descuento=tipo_descuento,
                monto_descuento=monto_descuento,
                estado_descuento=estado_descuento,
                fecha_vencimiento=fecha_vencimiento,
            )
            pun.save()

            cliente.puntos += Decimal(monto_descuento)
            cliente.save()
            messages.success(request, "Los puntos han sido creados correctamente.")
            return redirect('gestionarLealtad') 
        except Usuario.DoesNotExist:
            messages.error(request,'Error, Usuario No Existe')
            return redirect('gestionarLealtad') 
        
    return render(request, 'negocio/gestionarLealtad.html', {
        'cupones': cupones,
        'puntos': puntos,
        'search_email':search_email,
        'programa_lealtad_activo': programa_lealtad_activo,
        "color_scheme":color_scheme,
    })
    
# Despacho de pedidos

def despacho(request):
    color_scheme = get_color_scheme()
    return render(request,'negocio/despacho.html',{
        'color_scheme':color_scheme
    })


def despachoPedidos(request):
    # if 'correo_usuario' in request.session:
    color_scheme = get_color_scheme()
    pedidos = Pedido.objects.filter(estado_pedido = 'Pendiente')
    usuarios = Usuario.objects.filter(
        rol_usuario = 'Administrador Repartidor',
        estado_usuario = True
    )
    return render(request,'negocio/despachoPedidos.html',{
        'color_scheme':color_scheme,
        'pedidos':pedidos,
        'usuarios': usuarios
    })    
    # else:
    #     messages.error(request,'! Inicia Sesion Primero Para Acceder !')
    #     return redirect('login_negocio')

def asignarPedido(request):
    repartidor = request.POST.get('usuario','pendiente')
    id_pedido = request.POST.get('id_pedido','')
    if repartidor == 'pendiente':
        try:
            pedido = Pedido.objects.get(id_pedido = id_pedido)
        except Pedido.DoesNotExist:
            messages.error(request,'!Ocurrio Un Error!, Pedido no asignado')
            return redirect('despacho_pedidos')
        
        pedido.estado_pedido = 'pendiente'
        pedido.save()
        messages.success(request,'Pedido Asignado Como Pendiente')
        return redirect('despacho_pedidos')
    else:
        try:
            pedido = Pedido.objects.get(id_pedido = id_pedido)
        except Pedido.DoesNotExist:
            messages.error(request,'!Ocurrio un Error!, Pedido No Encontrado')
            return redirect('despacho_pedidos')
        
        try:
            usuario = Usuario.objects.get(correo = repartidor)
        except Usuario.DoesNotExist:
            messages.error(request,'!Ocurrio un Erro!, Usuario No Encontrado')
            return redirect('despacho_pedidos')
        
        pedido.estado_pedido = 'asignado'
        pedido.correo = usuario
        pedido.save()
        messages.success(request,'Pedido Asignado Correctamente')
        return redirect('despacho_pedidos')

def despachoPedidosAsignados(request):
    color_scheme = get_color_scheme()
    pedidos = Pedido.objects.filter(estado_pedido = 'asignado')
    return render(request,'negocio/pedidosAsignados.html',{
        'color_scheme':color_scheme,
        'pedidos':pedidos
    })

def despachoPedidosPendientes(request):
    color_scheme = get_color_scheme()
    pedidos = Pedido.objects.filter(estado_pedido = 'pendiente')
    return render(request,'negocio/pedidosPendientes.html',{
        'color_scheme':color_scheme,
        'pedidos':pedidos
    })


#configuracion empresa

#configuracion empresa

def cargar_configuracion():
    config_file_path = os.path.join(settings.BASE_DIR, 'config', 'configuracion_empresa.json')
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            return json.load(file)
    return {}

def guardar_configuracion(config):
    config_file_path = os.path.join(settings.BASE_DIR, 'config', 'configuracion_empresa.json')
    with open(config_file_path, 'w') as file:
        json.dump(config, file)

def configuracion_empresa_view(request):
    color_scheme = get_color_scheme()
    configuracion = cargar_configuracion()

    if request.method == 'POST':
        try:
            configuracion['nombre'] = request.POST.get('nombre', configuracion.get('nombre'))
            configuracion['slogan'] = request.POST.get('slogan', configuracion.get('slogan'))

            # Manejo de archivo de logo
            if request.FILES.get('logo'):
                logo_file = request.FILES['logo']

                # Verificar y crear el directorio logos si no existe
                logo_dir = os.path.join(settings.MEDIA_ROOT, 'logos')
                if not os.path.exists(logo_dir):
                    os.makedirs(logo_dir)

                # Guardar el archivo en el directorio logos
                logo_path = os.path.join(logo_dir, logo_file.name)
                with open(logo_path, 'wb+') as destination:
                    for chunk in logo_file.chunks():
                        destination.write(chunk)

                # Actualizar la ruta en el JSON
                configuracion['logo'] = f'/media/logos/{logo_file.name}'
            else:
                print("No se subió ningún archivo de logo.")

            guardar_configuracion(configuracion)

            # Guardar configuración en el archivo JSON
            guardar_configuracion(configuracion)

            # Redirigir para evitar reenvío de datos del formulario
            return redirect('configuracion_empresa')
        except Exception as e:
            print(f'Error al guardar la configuración: {e}')

    # Renderizar la vista inicial o después de un error
    return render(request, 'negocio/configuracion.html', {'configuracion': configuracion, 'color_scheme': color_scheme})

# Creacion de pepidos
def CrearPedidoAdministrador(request):
    color_scheme = get_color_scheme()
    return render(request,'negocio/registroPedido.html',{
        'color_scheme': color_scheme,
    })

