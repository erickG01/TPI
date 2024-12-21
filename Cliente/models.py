from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='direcciones') 
    nombre_direccion = models.CharField(max_length=50, null=True)
    departamento = models.CharField(max_length=50)
    numero_casa = models.IntegerField()
    municipio = models.CharField(max_length=50, null=True)
    calle = models.CharField(max_length=50)
    punto_referencia = models.CharField(max_length=50)

    class Meta:
        db_table = 'Direccion'
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
        ordering = ['id_direccion']

    def __str__(self):
        return f"{self.nombre_direccion} ({self.id_direccion})"


class Cliente(models.Model):
    correo_cliente = models.CharField(primary_key=True, max_length=50)
    nombre_cliente = models.CharField(max_length=50)
    telefono_cliente = models.CharField(max_length=15)
    password_cliente = models.CharField(max_length=128)  # Para almacenar contraseñas con hash
    puntos = models.IntegerField()
    imagen_cliente = models.ImageField(upload_to='imagen_cliente', null=True)

    class Meta:
        db_table = 'Cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['correo_cliente']

    def __str__(self):
        return f"{self.correo_cliente} - {self.nombre_cliente}"

    def set_password(self, raw_password):
        self.password_cliente = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_cliente)


class Reclamo (models.Model):
        id_reclamo=models.AutoField(primary_key=True)
        correo_cliente=models.ForeignKey(Cliente,on_delete=models.RESTRICT)
        descripcion_reclamo=models.CharField(max_length=100)
        fecha_reclamo=models.DateField()

        class Meta:
                db_table='Reclamo'
                verbose_name = 'Reclamo'
                verbose_name_plural = 'Reclamos'
                ordering=['id_reclamo']

        def __str__(self):
                texto = "{0} {1}"
                return texto.format(self.correo_cliente,self.id_reclamo)  



class Pago (models.Model):
        id_pago=models.AutoField(primary_key=True)
        correo_cliente=models.ForeignKey(Cliente,on_delete=models.RESTRICT)
        total_pago=models.DecimalField(max_digits=8, decimal_places=2)
        tipo_pago=models.CharField(max_length=15)

        class Meta:
                db_table='Pago'
                verbose_name = 'Pago'
                verbose_name_plural = 'Pagos'
                ordering=['id_pago']

        def __str__(self):
                texto = "{0} {1}"
                return texto.format(self.correo_cliente,self.id_pago)