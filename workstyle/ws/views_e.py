from workstyle.ws.models import TaskComment
from django.shortcuts import render_to_response

def insert_comment(request,object_id):
    message = None
    taskcomment = None
    try:
        taskcomment = TaskComment()
    except TaskComment.DoesNotExist:
        message = '対象のタスクが見つかりません'
    else:
        comment = request.POST.get('comment', None)
        commentator = request.POST.get('commentator', None)
        if not comment:
            message = comment
        else :
            taskcomment.comment_id = None
            taskcomment.contents = comment
            taskcomment.commentator = commentator
            taskcomment.task_id = object_id
            taskcomment.save()
    res = render_to_response('ws/xml/task.xml', {'task': taskcomment.task, 'message': message, 'mimetype': 'text/xml'})
    res['Content-Type'] = 'text/xml; charset=utf-8'
    return res