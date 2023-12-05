from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    programa = models.CharField(max_length=255)
    codigo_estudiantil = models.IntegerField(default=0)
    email = models.EmailField(max_length=255)
    
    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_horas = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.cantidad_horas} hora(s) el {self.fecha} a las {self.hora}'


class Penalizacion(models.Model):
    id_penalizacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return f'{self.usuario.nombre} - {self.fecha_inicio} a {self.fecha_fin}'

