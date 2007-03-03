# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from workstyle.ws.models import Task

import datetime, time

def parse_date_time(value=None):
    try:
        if value :
            value = value.replace('/', '-')
            try:
                return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6])
            except ValueError:
                try:
                    return datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M')[:5])
                except ValueError:
                    try:
                        return datetime.datetime(*time.strptime(value, '%Y-%m-%d')[:3])
                    except ValueError:
                        raise validators.ValidationError, gettext('Enter a valid date/time in YYYY/MM/DD HH:MM format.')
        return None
    except Exception, e:
        print e
        return None

#...
def update_task_property(request,  task_id):
    task = None
    message = None

    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        pass
    else:
        deadend_date = request.POST.get('deadEndDate', None)
        estimated_man_hour = request.POST.get('estimatedManHour', '0')
        
        task.estimated_man_hour = estimated_man_hour
        task.deadend_date = parse_date_time(deadend_date)
        task.save()
    
    res = render_to_response('ws/xml/task.xml', {'task': task, 'message': message, 'mimetype': 'text/xml'})
    res['Content-Type'] = 'text/xml; charset=utf-8'
    return res
