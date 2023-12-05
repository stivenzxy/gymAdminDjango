from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from gym.serializers import ReservaSerializer
from .models import User, Reserva, Penalizacion
from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, time, timedelta
from django.http import JsonResponse
import json


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        fixed_username = "admin"
        fixed_password = "1234"

        if username == fixed_username and password == fixed_password:
            
            user_data = {
                "username": fixed_username,
                "password": fixed_password,
            }

            return Response({"success": True, "message": "Login exitoso.", "data": user_data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Usuario o contraseña incorrectos."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CheckUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        uid = data.get('uid')

        # Realiza la consulta para verificar la existencia del usuario
        user_exists = User.objects.filter(uid=uid).exists()

        # Puedes devolver una respuesta JSON indicando si el usuario existe o no
        return Response({"user_exists": user_exists})

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Obtener datos de la solicitud POST
        data = json.loads(request.body)
        uid = data.get('uid')
        nombre = data.get('nombre')
        programa = data.get('programa')
        codigo_estudiantil = data.get('codigo')
        email = data.get('email')

        try:
            # Verificar si el usuario ya existe
            user_existente = User.objects.get(uid=uid)
            return Response({"success": False, 'message': 'El usuario ya existe.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # Crear un nuevo usuario
            nuevo_usuario = User.objects.create(
                uid=uid,
                nombre=nombre,
                programa=programa,
                codigo_estudiantil=codigo_estudiantil,
                email=email
            )
            return Response({"success": True, "message": "Usuario creado con éxito."}, status=status.HTTP_201_CREATED)
        

class ReporteView(View):
    def get(self, request, *args, **kwargs):
        # Obtener las reservas de la base de datos
        reservas = Reserva.objects.all()

        # Crear un DataFrame de pandas con los datos de las reservas
        data = {
            'Nombre': [reserva.usuario.nombre for reserva in reservas],
            'Programa': [reserva.usuario.programa for reserva in reservas],
            'Código Estudiantil': [reserva.usuario.codigo_estudiantil for reserva in reservas],
            'Fecha': [reserva.fecha for reserva in reservas],
            'Hora': [reserva.hora for reserva in reservas],
            'Cantidad de Horas': [reserva.cantidad_horas for reserva in reservas],
        }

        df = pd.DataFrame(data)

        # Crear un libro de Excel y escribir el DataFrame en una hoja
        wb = Workbook()
        ws = wb.active

        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Configurar las columnas para un mejor formato
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Configurar la respuesta HTTP para la descarga del archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reservas.xlsx'
        wb.save(response)

        return response


class CreateReservaView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del cuerpo de la solicitud
            data = json.loads(request.body)
            uid = data.get('uid')
            fecha_reserva = datetime.strptime(request.data.get('fecha_reserva'), '%Y-%m-%d')  #cambiar fecha por fecha_reserva
            fecha_actual = datetime.strptime(request.data.get('fecha_actual'), '%Y-%m-%d') 
            hora = datetime.strptime(data.get('hora'), '%H:%M').time()  
            cantidad_horas = data.get('cantHoras')
            usuario = User.objects.get(uid=uid)

            # Validar penalización
            
            penalizaciones = Penalizacion.objects.filter(usuario=usuario)
            
            for penalizacion in penalizaciones:
                fecha_inicio_str = penalizacion.fecha_inicio.strftime('%Y-%m-%d')
                fecha_fin_str = penalizacion.fecha_fin.strftime('%Y-%m-%d')

                if datetime.strptime(fecha_inicio_str, '%Y-%m-%d') <= fecha_actual <= datetime.strptime(fecha_fin_str, '%Y-%m-%d'):
                    return Response({"success": False, "message": f"Estás penalizad@, no puedes reservar, puedes volver a reservar el {fecha_fin_str}."})
            
            # Validar el aforo
            aforo_max = 3
            # Calcular el intervalo de tiempo para la nueva reserva
            inicio_nueva_reserva = datetime.combine(fecha_reserva, hora)
            fin_nueva_reserva = inicio_nueva_reserva + timedelta(hours=cantidad_horas)

            # Verificar si hay reservas existentes que se superponen
            reservas_superpuestas = Reserva.objects.filter(
                fecha=fecha_reserva,
                hora__lt=fin_nueva_reserva,
                hora__gte=inicio_nueva_reserva
            )

                        # Calcular el aforo ocupado en el intervalo de la nueva reserva
            aforo_ocupado = sum(reserva.cantidad_horas for reserva in reservas_superpuestas)

            # Verificar si el aforo estaría completo después de agregar la nueva reserva
            if aforo_ocupado >= aforo_max:
                return Response({"success": False, "message": "Aforo completo para este intervalo de tiempo."})

           # Verificar si al agregar la nueva reserva, el aforo estaría completo en alguna parte del intervalo
            for reserva in reservas_superpuestas:
                reserva_inicio = datetime.combine(reserva.fecha, reserva.hora)
                reserva_fin = reserva_inicio + timedelta(hours=reserva.cantidad_horas)

                if (
                    inicio_nueva_reserva <= reserva_inicio < fin_nueva_reserva or
                    inicio_nueva_reserva < reserva_fin <= fin_nueva_reserva
                ):
                    return Response({"success": False, "message": "Aforo completo para este intervalo de tiempo."})
                                
            # Validar Horario

            hora_fin = datetime.combine(fecha_reserva, hora) + timedelta(hours=cantidad_horas)
            hora_fin = hora_fin.time()

            if (
                (fecha_reserva.weekday() in [0, 4] and (time(8, 0) <= hora <= time(17, 0)) and (time(8, 0) <= hora_fin <= time(17, 0))) or
                (fecha_reserva.weekday() in [1, 2, 3] and (time(8, 0) <= hora <= time(15, 0)) and (time(8, 0) <= hora_fin <= time(15, 0)))
            ):
                # Crear la reserva
                reserva = Reserva.objects.create(
                    usuario=usuario,
                    fecha=fecha_reserva,
                    hora=hora,
                    cantidad_horas=cantidad_horas
                )

                return Response({"success": True, "message": "Reserva creada con éxito."})
            else:
                return Response({"success": False, "message": "El horario no está dentro del rango permitido."}, status=400)
        
        except User.DoesNotExist:
            return Response({"success": False, "message": "El usuario no existe."}, status=400)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)
    

class GetReservasView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todas las reservas
            reservas = Reserva.objects.all()
            serializer = ReservaSerializer(reservas, many=True)

            return Response({'success': True, 'reservas': serializer.data})
        
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)
        

class ReservasPorUsuarioView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el uid del parámetro de consulta
            uid = request.query_params.get('uid')

            # Validar si el usuario existe
            usuario = User.objects.get(uid=uid)

            # Obtener las reservas para el usuario
            reservas_usuario = Reserva.objects.filter(usuario=usuario)
            serializer = ReservaSerializer(reservas_usuario, many=True)

            return JsonResponse({'success': True, 'reservas': serializer.data})
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El usuario no existe.'}, status=400)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        

class PenalizarView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            reserva_id = request.data.get('id')
            fecha_inicio = datetime.strptime(request.data.get('fecha'), '%Y-%m-%d')
            fecha_fin = fecha_inicio + timedelta(days=7)
            reserva = Reserva.objects.get(id_reserva=reserva_id)
            reserva_uid = reserva.usuario.uid
            usuario = User.objects.get(uid = reserva_uid)

            penalizacion = Penalizacion.objects.create(
                    usuario=usuario,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                )
            
            reserva.delete()

            return Response({'success': True, 'message': 'Reserva penalizada y eliminada'})
        
        except Reserva.DoesNotExist:
            return Response({'success': False, 'message': 'Reserva no encontrada'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)



