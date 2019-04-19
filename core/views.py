from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.apiviews import InfoSchedules
import requests
import datetime
import json


@csrf_exempt
def get_events(request):
    events_month = []
    now = datetime.datetime.now()
    result = InfoSchedules().get(request, None, now.month, now.year, None)
    result = json.loads(json.dumps(result.data.serializer.data))

    for res in result:
        print(res)
        events_month.append({
            'id':res['id'],
            'title':res['author'],
            'start':str(res['date_schedule']) + 'T' + str(res['module']['start']),
            'end':str(res['date_schedule']) + 'T' + str(res['module']['end']),
        })
    

    return JsonResponse(events_month, safe=False)



    
    
