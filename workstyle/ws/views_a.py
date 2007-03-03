# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from workstyle.ws.models import Task

import datetime

#...
def update_task_property(request,  task_id):
    task = None
    message = None

    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        pass
    else:
        deadend_date = request.POST['deadEndDate']
        estimated_man_hour = request.POST['estimatedManHour']
        
        
        task.estimated_man_hour = estimated_man_hour
        
        tmp1 = deadend_date.replace("/", " ")
        tmp2 = tmp1.replace(":", " ")
        date_l = tmp2.split(" ") 
        task.deadend_date = datetime.datetime (int(date_l[0]), int(date_l[1]), int(date_l[2]), int(date_l[3]), int(date_l[4]), int(date_l[5]))
        
        task.save()
    
    res = render_to_response('ws/xml/task.xml', {'task': task, 'message': message, 'mimetype': 'text/xml'})
    res['Content-Type'] = 'text/xml; charset=utf-8'
    return res
