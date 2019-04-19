from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from schedule.serializers import ScheduleSerializer, UserProfileSerializer
from schedule.models import Schedule, UserProfile


class InfoSchedules(APIView):
    """
    Trae información sobre las reservas activas, según fecha.
    Este endpoint soporta 3 parametros:
        **year** -- Respresenta el año de la reserva, permite obtener todas las reservas en un año en específico
        **month** -- Representa el mes de la reserva, permite obtener todas las reservas de un mes en específico. Es necesario incluir en año
        **day** -- Representa el día de la reserva, permite obtener todas las reservas de un día en específico. Es necesario incluir en año y el mes         
    
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, day=None, month=None, year=None, format=None):
        schedule = Schedule.objects
        if day is not None and month is not None and year is not None:
            schedule = schedule.filter(date_schedule__year=year, date_schedule__month=month, date_schedule__day=day)

        elif month is not None and year is not None:
            schedule = schedule.filter(date_schedule__year=year, date_schedule__month=month)

        elif year is not None:
            schedule = schedule.filter(date_schedule__year=year)
        else:
            schedule = schedule.all()
        
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)


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