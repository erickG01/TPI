from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from Cliente import views
from Negocio.views import *
from django.views.generic import TemplateView
from Repartidor.views import *
from django.contrib.auth import views as auth_views

from django.urls import re_path
from django.views.static import serve

from Negocio.views import configuracion_empresa_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #Redireccion
    path('',lambda request: redirect('login_cliente')),
    path('manifest.json',views.manifest, name='manifest'),
    path('repartidor/', lambda request: redirect('login_repartidor'), name='redirect_repartidor'),
    # Rutas para la PWA Repartidor

    #Negocio Vistas
    #path('', include('pwa.urls')),
    #Cambio Colores
    path('negocio/cambiarColores',cambiarColores,name='colores_negocio'),
    #Negocio
    path('negocio/login',Login,name='login_negocio'),
    path('negocio/Administrador',InicioAdministrador,name='inicio_negocio_administrador'),
    path('negocio/Menu',InicioMenu,name='inicio_negocio_menu'),
    path('negocio/cerrarSesion',CerrarSesionNegocio,name='cerrar_sesion_negocio'),
    path('negocio/perfil',Perfil_Usuario,name='negocio_perfil'),
    path('negocio/actualizarPerfil',ActualizarPerfil,name='actualizar_perfil'),
    path('negocio/gestionar/<str:gestion>',gestionarUsuarios,name='gestionUsuarios'),
    path('negocio/registrar/<str:gestion>',Registrar,name='registrar_usuario'),

    #configuracion
    path('negocio/configuracion/', configuracion_empresa_view, name='configuracion_empresa'),
    #contraseña

    path('negocio/actualizarUsuario/<str:gestion>',actualizarUsuario,name='actualizarUsuario'),
    path('negocio/buscarUsuario/<str:gestion>',BuscarUsuario,name='buscarUsuario'),
    path('negocio/preferencias',Preferencias,name='preferencias'),
    path('negocio/soporte',Soporte,name='soporte'),
    path('negocio/recuperarClave',recuperarClave,name='recuperar_negocio_clave'),
    path('negocio/mandarCorreo',EnviarCorreo,name='enviar_correo'),
    path('negocio/restablecer',vistaRestablecer,name='restablecer_negocio'),
    path('negocio/lealtad',gestionarLealtad,name='gestionarLealtad'),
    #Negocio Operaciones CRUD
    path('negocio/iniciarSesion',IniciarSesion,name='iniciar_sesion_negocio'),
    path('negocio/actualizar',ActualizarUsuario,name='actualizar_negocio'),
    path('negocio/crearUsuario',crearUsuario,name='crear_usuario_negocio'),
    path('negocio/editarUsuario/<str:gestion>',editarUsuario,name='actualizar_usuario_negocio'),
    #Pedidos
    path('negocio/despacho',despacho,name='inicio_despacho'),
    path('negocio/despacho/pedidos',despachoPedidos,name='despacho_pedidos'),
    path('negocio/despacho/asignados',despachoPedidosAsignados,name='despacho_asignados'),
    path('negocio/despacho/pendientes',despachoPedidosPendientes,name='despacho_pendientes'),
    path('negocio/asignarPedido',asignarPedido,name='negocio_asignar_pedido'),
     path('negocio/configuracion/', configuracion_empresa_view, name='configuracion_empresa'),
    #Registrar Pedidos
    #Menu
    path('negocio/menu/productos',inicioProductos,name='inicio_producto'),
    path('negocio/menu/crearMenu',crearMenu,name='crear_menu'),
    path('negocio/menu/crear_producto',crearProducto,name='crear_producto'),
    path('negocio/menu/editar_producto',actualizarProducto,name='actualizar_producto'),
    path('negocio/menu/crearMenu_DetalleMenu',CrearMenu_DetalleMenu,name='crearMenu_DetalleMenu'),
    path('negocio/menu/menus_disponibles',MenusDisponibles,name='menus_disponibles'),
    path('negocio/menu/eliminarMenu',EliminarMenu,name='eliminar_menu'),
    #Endpoints
    path('negocio/api/menu',Menu_Detalle_Menu,name='lista_menu'),
    path('negocio/api/detalleMenu',filtarMenuDetalle,name='lista_detalle_menu'),


    #Cliente
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('editar_cliente/', views.editar_cliente, name='editar_cliente'),
    path('login_cliente/', views.login_cliente, name='login_cliente'),
    path('logout/', views.logout_cliente, name='logout_cliente'),
    path('reclamos', views.reclamos, name='reclamos'),
    path('productos/', views.productos, name='productos'),
  #Carrito de compras
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:id_producto>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/eliminar/', views.eliminar_del_carrito, name='vaciar_carrito'),
    path('carrito/actualizar/<int:id_producto>/<int:nueva_cantidad>/', views.actualizar_carrito,name='actualizar_carrito'),
    path('registrar_pedido/', views.registrar_pedido, name='registrar_pedido'),
    path('cliente/cupones', views.cupones_cliente, name='cupones_cliente'),
    path('cliente/eliminar_descuento', views.eliminar_descuento, name='eliminar_descuento'),
    path('cliente/generar-factura/', views.generar_factura, name='generar_factura'),





  #Direcciones
    path('mapa/', views.mapa, name='mapa'),
    path('crear-direccion/', views.crear_direccion, name='crear_direccion'),
    path('direcciones', views.mostrar_direcciones, name='direcciones'),
    path('eliminar-direccion/<int:id_direccion>/', views.eliminar_direccion, name='eliminar_direccion'),
    path('direccion/editar/<int:id_direccion>/', views.editar_direccion, name='editar_direccion'),
    path('api/direcciones/', views.obtener_direcciones, name='obtener_direcciones'),
    path('comida/', views.comida, name='comida'), 
    path('gestionar-reclamos/', views.gestionar_reclamos, name='gestionar_reclamos'),
    path('menu_Diario/', views.menu_diario, name='menu_Diario'),


   #Repartidor
    path('repartidor/login', login_repartidor, name='login_repartidor'),
    path('repartidor/pedidos', pedidos_asignados, name='pedidos_asignados'),
    path('repartidor/logout', cerrar_sesion, name='cerrar_sesion'),
    path('repartidor/activar/',activar_repartidor, name='activar_repartidor'),
    path('repartidor/desactivar/',desactivar_repartidor, name='desactivar_repartidor'),
    path('repartidor/perfil/',perfil_usuario, name='perfil_usuario'),
    path('repartidor/detalle_pedido/<int:pedido_id>/',obtener_detalle_pedido, name='detalle_pedido'),
    path('repartidor/entregar_pedido/<int:pedido_id>/', entregar_pedido, name='entregar_pedido'),
    path('repartidor/listar_pedidos/',listar_pedidos_pendientes, name='listar_pedidos'),
    path('repartidor/asignar_pedido/<int:pedido_id>/',asignar_pedido, name='asignar_pedido'),
    path('repartidor/no_entregado/<int:pedido_id>/',marcar_no_entregado, name='marcar_no_entregado'),
    #cambio de contraseña
    path('cambiar-contraseña/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('cambiar-contraseña/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

