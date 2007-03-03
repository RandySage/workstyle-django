from workstyle.ws.models import Task
from django.shortcuts import render_to_response
from django.template import RequestContext

def update_tag(request,object_id):
    message = None
    task = None
    try:
        task = Task.objects.get(pk=object_id)
    except Task.DoesNotExist:
        message = 'dame'
    else:
        tags = request.POST.get('tagList', None)
        if not tags:
            message = 'dame'
        else :
            task.tag_list = tags
            task.save()
    res = render_to_response('ws/xml/task.xml', {'task': task, 'message': message, 'mimetype': 'text/xml'},context_instance=RequestContext(request))
    res['Content-Type'] = 'text/xml; charset=utf-8'
    return res