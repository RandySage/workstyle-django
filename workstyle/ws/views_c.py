from workstyle.ws.models import Task
from django.shortcuts import render_to_response

def update_contents(request,object_id):
    message = None
    task = None
    try:
        task = Task.objects.get(pk=object_id)
    except Task.DoesNotExist:
        message = '対象のタスクが見つかりません'
    else:
        contents = request.POST.get('contents', None)
        if not contents:
            message = 'タスク本文は必須です'
        else :
            task.contents = contents
            task.save()
    res = render_to_response('ws/xml/task.xml', {'task': task, 'message': message, 'mimetype': 'text/xml'})
    res['Content-Type'] = 'text/xml; charset=utf-8'
    return res