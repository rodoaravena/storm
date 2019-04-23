from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from schedule.serializers import ScheduleSerializer, UserProfileSerializer
from schedule.models import Schedule, UserProfile
from datetime import datetime, timedelta


class InfoSchedules(APIView):
    """
    Trae información sobre las reservas activas, según fecha.
    Este endpoint soporta 3 parametros:
        **year** -- Respresenta el año de la reserva, permite obtener todas las reservas en un año en específico
        **month** -- Representa el mes de la reserva, permite obtener todas las reservas de un mes en específico. Es necesario incluir en año
        **day** -- Representa el día de la reserva, permite obtener todas las reservas de un día en específico. Es necesario incluir en año y el mes         
    
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, day=None, month=None, year=None, format='json'):
        schedule = Schedule.objects
        if day is not None and month is not None and year is not None:
            schedule = schedule.filter(date_schedule_start__year=year, date_schedule_start__month=month, date_schedule_start__day=day)

        elif month is not None and year is not None:
            schedule = schedule.filter(date_schedule_start__year=year, date_schedule_start__month=month)

        elif year is not None:
            schedule = schedule.filter(date_schedule_start__year=year)
        else:
            schedule = schedule.all()
        
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

class InfoAvailableRoomHours(APIView):
    """
    Trae información sobre los horarios dispobibles de la sala activas, en el día.
    Este endpoint soporta 3 parametros:
        **year** -- Respresenta el año de la reserva, permite obtener todas las reservas en un año en específico
        **month** -- Representa el mes de la reserva, permite obtener todas las reservas de un mes en específico. Es necesario incluir en año
        **day** -- Representa el día de la reserva, permite obtener todas las reservas de un día en específico. Es necesario incluir en año y el mes         
        ** * ** -- Posteriormente soportará la sala a solicitar
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

    def get(self, request, year, month, day, format=None):
        list_hours = [
            '08:30','09:00',
            '09:30','10:00',
            '10:30','11:00',
            '11:30','12:00',
            '12:30','13:00',
            '13:30','14:00',
            '14:30','15:00',
            '15:30','16:00',
            '16:30','17:00',
            '17:30','18:00',
            '18:30','19:00',
            '19:30','20:00',
            '20:30','21:00',
            '21:30',
        ]
        data = {}
        busy_hours = []
        available_hours = []
        schedules = Schedule.objects.filter(date_schedule_start__year=year, date_schedule_start__month=month, date_schedule_start__day=day)
        for h in list_hours:
            for s in schedules:
                start = timezone.localtime(s.date_schedule_start)
                end = timezone.localtime(s.date_schedule_end)
                hora = datetime.strptime(h, '%H:%M')
                if start.time() <= hora.time() < end.time():
                    busy_hours.append(h)
        for h_a in list_hours:
            if h_a not in busy_hours:
                available_hours.append(h_a)

        data['available_hours'] = available_hours
        
        return Response(data)

class InfoRangeRoomHours(APIView):
    """
    Trae información sobre los horarios dispobibles de la sala activas, en el día.
    Este endpoint soporta 3 parametros:
        **year** -- Respresenta el año de la reserva, permite obtener todas las reservas en un año en específico
        **month** -- Representa el mes de la reserva, permite obtener todas las reservas de un mes en específico. Es necesario incluir en año
        **day** -- Representa el día de la reserva, permite obtener todas las reservas de un día en específico. Es necesario incluir en año y el mes         
        ** hour ** -- Representa la hora 
        ** * ** -- Posteriormente soportará la sala a solicitar
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    

    def get(self, request, year, month, day, hour, min, format=None):
        list_hours = []
        data = {}
        busy_hours = []
        range_hours = []
        end_hour = datetime.strptime(hour+":"+min, '%H:%M')
        print(end_hour)
        while True:
            end_hour = end_hour + timedelta(minutes=30)
            h = "0"+str(end_hour.hour) if int(end_hour.hour) < 10 else str(end_hour.hour)
            m = "0"+str(end_hour.minute) if int(end_hour.minute) < 10 else str(end_hour.minute)
            list_hours.append(h+":"+m)
            if end_hour.hour == 22 and end_hour.minute == 0:
                break

        schedules = Schedule.objects.filter(date_schedule_start__year=year, date_schedule_start__month=month, date_schedule_start__day=day)
        for h in list_hours:
            for s in schedules:
                start = timezone.localtime(s.date_schedule_start)
                end = timezone.localtime(s.date_schedule_end)
                hora = datetime.strptime(h, '%H:%M')
                if start.time() <= hora.time() < end.time():
                    busy_hours.append(h)
                        
        for h_a in list_hours:
            if h_a not in busy_hours:
                range_hours.append(h_a)
            else:
                range_hours.append(h_a)
                break

        data['range_hours'] = range_hours
        
        return Response(data)
        



class RegisterUser(APIView):
    def post(self, request, format=None):
        data_response = {}
        status_code = 0
        userprofile = UserProfile(rut=request.data['rut'])
        if userprofile.create_user(request.data['username'],request.data['password'], request.data['name'], request.data['lastname']):
            serializer = UserProfileSerializer(userprofile)
            data_response['response'] = 'Usuario creado'
            data_response['data'] = serializer.data
            status_code = status.HTTP_201_CREATED
        else:
            data_response['response'] = 'Error al intentar crear al usuario'
            data_response['data'] = ''
            status_code = status.HTTP_409_CONFLICT
        
        return Response(data_response, status=status_code)

class InfoUser(APIView):
    def get(self, request, rut_user, format=None):
        userprofile = UserProfile.objects.get(rut=rut_user)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)