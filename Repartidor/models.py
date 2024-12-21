from django.db import models
# Create your models here.
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    correo = models.ForeignKey('Negocio.Usuario',on_delete=models.RESTRICT)
    id_direccion = models.ForeignKey('Cliente.Direccion',on_delete=models.RESTRICT)
    id_pago = models.ForeignKey('Cliente.Pago',on_delete=models.RESTRICT)
    estado_pedido = models.CharField(max_length=15)
   
    class Meta:
        db_table = 'Pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.id_pedido,self.id_direccion)
    
class Detalle_Producto(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Negocio.Producto',on_delete=models.RESTRICT)
    id_pedido = models.ForeignKey(Pedido,on_delete=models.RESTRICT)
    cantidad_detalle = models.IntegerField(null=True)

    class Meta:
        db_table = 'Detalle Producto'
        verbose_name = 'Detalle Producto'
        verbose_name_plural = 'Detalle Productos'
    
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.id_detalle,self.id_producto)