from django.contrib import admin
from .models import  User, Reserva, Penalizacion

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'programa', 'codigo_estudiantil', 'email', 'uid')
    search_fields = ('nombre', 'codigo_estudiantil', 'uid')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'hora', 'cantidad_horas', 'id_reserva')
    list_filter = ('usuario', 'fecha')
    search_fields = ('usuario__codigo_estudiantil', 'fecha')

@admin.register(Penalizacion)
class PenalizacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_fin', 'id_penalizacion')
    search_fields = ('usuario__codigo_estudiantil','id_penalizacion')