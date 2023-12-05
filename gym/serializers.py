from rest_framework import serializers
from .models import User, Reserva, Penalizacion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'nombre', 'programa', 'codigo_estudiantil', 'email')

class ReservaSerializer(serializers.ModelSerializer):
    
    usuario = UserSerializer()  

    class Meta:
        model = Reserva
        fields = ('id_reserva', 'usuario', 'fecha', 'hora', 'cantidad_horas')

class PenalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalizacion
        fields = '__all__'


