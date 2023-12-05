# utils.py
import datetime


def validar_fecha_hora(fecha, hora_inicio, duracion):
    try:
        fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio_obj = datetime.datetime.strptime(hora_inicio, '%H:%M').time()
        duracion_obj = datetime.timedelta(hours=int(duracion))

        # Verificar que la fecha sea mayor o igual a la fecha actual
        if fecha_obj < datetime.datetime.now().date():
            return False

        # Verificar que la hora de inicio sea válida
        if hora_inicio_obj < datetime.datetime.now().time():
            return False

        # Verificar que la duración sea mayor a cero
        if duracion_obj <= datetime.timedelta():
            return False

        return True
    except ValueError:
        return False