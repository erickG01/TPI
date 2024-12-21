import uuid
from django.db import models


def get_image_filename_usuario(instance, filename):
    ext = filename.split('.')[-1]
    return f'usuarios/{uuid.uuid4()}.{ext}'

def get_image_filename_producto(instance, filename):
    ext = filename.split('.')[-1]
    return f'productos/{uuid.uuid4()}.{ext}'

# Create your models here.
class Usuario(models.Model):
    correo = models.CharField(primary_key=True,max_length=50)
    nombre_usuario = models.CharField(max_length=50)
    rol_usuario = models.CharField(max_length=50)
    password_usuario = models.CharField(max_length=9)
    estado_usuario = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to=get_image_filename_usuario,null=True,blank=True,default='usuarios/usuario_defecto.png')

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        texto = "{0} {1} Rol: {2}"
        return texto.format(self.correo,self.nombre_usuario,self.rol_usuario)
    
class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)
    correo = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    fecha_menu = models.DateField(auto_now=False)

    class Meta:
        db_table = 'Menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        texto = "Id Menu: {0} Correo: {1}"
        return texto.format(self.id_menu,self.correo)
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    correo = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    nombre_producto = models.CharField(max_length=50)
    precio_producto = models.DecimalField(max_digits=8,decimal_places=2)
    disponibilidad_producto = models.BooleanField(default=False)
    descripcion_producto = models.CharField(max_length=100)
    imagen_producto = models.ImageField(upload_to=get_image_filename_producto,null=True,blank=True,default='productos/producto_defecto.png')

    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.id_producto,self.nombre_producto)


class Detalle_Menu(models.Model):
    id_detalle_menu = models.AutoField(primary_key=True)
    id_menu = models.ForeignKey(Menu,on_delete=models.RESTRICT)
    id_producto = models.ForeignKey(Producto,on_delete=models.RESTRICT)

    class Meta:
        db_table = 'Detalle Menu'
        verbose_name = 'Detalle Menu'
        verbose_name_plural = 'Detalle Menus'

    def __str__(self):
        texto = "Id Detalle: {0} Id Menu: {1} Id Producto: {2}"
        return texto.format(self.id_detalle_menu,self.id_detalle_menu,self.id_producto)
    

class Descuento(models.Model):
    id_descuento = models.AutoField(primary_key=True)
    correo = models.ForeignKey(Usuario,on_delete=models.RESTRICT)
    correo_cliente = models.ForeignKey('Cliente.Cliente',on_delete=models.RESTRICT)
    tipo_descuento = models.CharField(max_length=15)
    monto_descuento = models.DecimalField(max_digits=8,decimal_places=2)
    estado_descuento = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField()

    class Meta:
        db_table = 'Descuentos'
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'

    def __str__(self):
        texto = "{0} {1} {2}"
        return texto.format(self.id_descuento,self.correo_cliente,self.estado_descuento)