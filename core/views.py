from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.apiviews import InfoSchedules
import requests
import datetime
import json

def index(request):
    template_name = 'index.html'
    context = {}
    return render(request, template_name,context)


@csrf_exempt
def get_events(request):
    events_month = []
    result = InfoSchedules().get(request, None, None, None, None)
    result = json.loads(json.dumps(result.data.serializer.data))

    for res in result:
        events_month.append({
            'id':res['id'],
            'title':res['author'],
            'start':str(res['date_schedule_start']),
            'end':str(res['date_schedule_end']),
        })   

    return JsonResponse(events_month, safe=False)



    
    
