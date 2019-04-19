from django.conf import settings # import the settings file

def application_name(request):
    # devieve el nombre de la aplicación
    return {'application_name': settings.APPLICATION_NAME}