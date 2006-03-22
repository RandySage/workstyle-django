# Create your views here.
# python library
import string
from datetime import datetime, timedelta
import urllib

# django library
from django import forms
from django.db.models.query import Q
from django import template
from django.template import loader, Context
from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import ObjectPaginator, InvalidPage

# workstyle library
from WorkStyle.workstyle.models import Task, Tag, TagList, Attachment, Comment, TAG_TYPE_CHOICES, TASK_STATUS
from WorkStyle.settings import WORKSTYLE_ROOT, WORKSTYLE_JUNK_DIR, LANGUAGE_CODE
from WorkStyle.workstyle.view.tag import getStatusList, getTagTypeList, recreateTask
from WorkStyle.workstyle.manipulators import TaskManipulator
from WorkStyle.workstyle.util import get_id_list_from_url
from WorkStyle.workstyle.templatetags import wsfilters

def index(request, task_id):
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404

    tag_list = Tag.objects.filter(visible__exact=True)
    status_list = getStatusList()

    attach_list = task.attachment_set.all()
    task_taglist_list = task.taglist_set.all()
    task_tag_list = []
    for taglist in task_taglist_list:
        task_tag_list.append(taglist.tag)
    comment_list = task.comment_set.all()

    tag_with_selected_list = []
    for tag in tag_list :
        tag_with_selected = TaskTag(tag.id, tag.name, tag.tag_type, tag.visible)
        tag_with_selected_list.append(tag_with_selected)
        for task_tag in task_tag_list :
            if tag.id == task_tag.id :
                tag_with_selected.selected = True

    return render_to_response('workstyle/TaskDetail',{'task': task, 'tag_list': tag_list,'status_list': status_list,'attach_list': attach_list,'task_tag_list': task_tag_list,'comment_list': comment_list, 'tag_with_selected_list': tag_with_selected_list, 'workstyle_root': WORKSTYLE_ROOT })

def top(request) :
    try:
        del request.session['prev_search']
    except KeyError:
        pass    
    return list_default(request)

def list_default(request):
    redirect_to = request.session.get('prev_search', (WORKSTYLE_ROOT + '/TaskList/%s/%s/%s/%s/%s/%s/%s' % (0, 0, 0, 0, 0, 50, '-')))
    return HttpResponseRedirect(redirect_to)


def list_update_status(request, sort_type, sort_order, status_list, tag_list, offset, limit, key, task_id, status) :
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404
    task.status = status
    task.update_date = datetime.now()
    task.save()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/TaskList/%s/%s/%s/%s/%s/%s/%s' % (sort_type, sort_order, status_list, tag_list, offset, limit, key))

def list_delete_task(request, sort_type, sort_order, status_list, tag_list, offset, limit, key, task_id) :
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404
    task.delete()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/TaskList/%s/%s/%s/%s/%s/%s/%s/' % (sort_type, sort_order, status_list, tag_list, offset, limit, key))

def list(request, sort_type, sort_order, status_list, tag_list, offset, limit, key) :
    request.session['prev_search'] = '/WorkStyle/TaskList/%s/%s/%s/%s/%s/%s/%s/' % (sort_type, sort_order, status_list, tag_list, offset, limit, key)

    task_list, all_count = get_task_list(sort_type, sort_order, status_list, tag_list, offset, limit, key, None)

    task_bean_list = _get_task_bean_list(task_list)

    tags_list = Tag.objects.filter(visible__exact=True)
    statuses_list = getStatusList()

    status_list_array = get_id_list_from_url(status_list)
    for status in statuses_list :
        for selected_status in status_list_array :
            if status.id == selected_status :
                status.selected = True

    tag_list_array = get_id_list_from_url(tag_list)
    search_tag_list = []
    for tag in tags_list :
        search_tag = TaskTag(tag.id, tag.name, tag.tag_type, tag.visible)
        for selected_tag in tag_list_array :
            if tag.id == selected_tag :
                search_tag.selected = True
        search_tag_list.append(search_tag)
    result_count = len(task_bean_list)
    start = int(offset)
    end = start + result_count
    start = start + 1
    prev = "0"
    next = "0"
    if start > 1 :
        prev = "1"
    if end < all_count :
        next = "1"
    search_query = '/%s/%s/%s/%s/%s/%s/%s/' % (sort_type, sort_order, status_list, tag_list, offset, limit, urllib.quote_plus(key))
    domain = request.META['SERVER_NAME']
    port = request.META['SERVER_PORT']
    if port != "80" and port != "0" and port != 80 and port != 0:
        domain += ":" + port
    return render_to_response('workstyle/TaskList',{'task_list': task_bean_list,
                                          'tag_list': search_tag_list,
                                          'status_list': statuses_list, 
                                          'key': key,
                                          'sort_type': sort_type,
                                          'sort_order': sort_order,
                                          'offset': offset,
                                          'limit': limit,
                                          'start': start,
                                          'end': end,
                                          'prev': prev,
                                          'next': next,
                                          'all_count': all_count,
                                          'domain': domain,
                                          'workstyle_root': WORKSTYLE_ROOT,
                                          'search_query': search_query })

def list_rss(request, sort_type, sort_order, status_list, tag_list, offset, limit, key) :
    task_list, all_count = get_task_list(sort_type, sort_order, status_list, tag_list, offset, limit, key, datetime.now())
    domain = request.META["SERVER_NAME"]
    port = request.META["SERVER_PORT"]
    if port != "80" :
        domain += ":" + port
    response = HttpResponse(mimetype='text/xml')
    t = loader.get_template('workstyle/rss10')

    c = Context({
        'task_list': task_list,
        'domain': domain,
        'workstyle_root': WORKSTYLE_ROOT,
    })
    response.write(t.render(c))
    return response

def list_atom(request, sort_type, sort_order, status_list, tag_list, offset, limit, key) :
    task_list, all_count = get_task_list(sort_type, sort_order, status_list, tag_list, offset, limit, key, datetime.now())
    task_bean_list = _get_task_bean_list(task_list)
    statuses_list = getStatusList()

    domain = request.META["SERVER_NAME"]
    port = request.META["SERVER_PORT"]
    if port != "80" :
        domain += ":" + port

    search_query = '/%s/%s/%s/%s/%s/%s/%s/' % (sort_type, sort_order, status_list, tag_list, offset, limit, urllib.quote_plus(key))

    response = HttpResponse(mimetype='text/xml')
    t = loader.get_template('workstyle/atom')

    c = Context({
        'task_list': task_bean_list,
        'status_list': statuses_list,
        'domain': domain,
        'search_key': search_query,
        'workstyle_root': WORKSTYLE_ROOT,
        'language_code': LANGUAGE_CODE,
    })
    response.write(t.render(c))
    return response
    

def get_task_list(sort_type, sort_order, status_list, tag_list, offset, limit, key, today) :
    query = {}
    query = _get_criteria_sort(query, sort_type, sort_order)
    query = _get_criteria_status(query, status_list)
    query = _get_criteria_tag(query, tag_list)
    print query
    if key == "" or key == "-" :
        pass
    else :
        query['task__contains'] = key
    # for count select

    all_count = Task.objects.filter(**query).count()

    result_list = None
    if today :
        yesterday = today + timedelta(-1)
        query['update_date__range'] = (yesterday, today)
        result_list = Task.objects.filter(**query)
    else :
        query_offset = 0
        query_limit = 50
        if offset != "0" and limit != "0" :
            query_offset = int(offset)
        if limit != "0" :
            query_limit = query_offset + int(limit)
        result_list = Task.objects.filter(**query)[query_offset: query_limit]
    return result_list, all_count

def _get_criteria_tag(query, tag_list) :
    tag_id_list = get_id_list_from_url(tag_list)
    if len(tag_id_list) == 0 :
        return query
    tag_list = Tag.objects.filter(id__in=tag_id_list)

    if(len(tag_list) == 0) :
        return query
    simple = len(tag_list) == 0
    if simple :
        query['tag_searchable__contains'] = tag_list[0].name
        return query
    
    for i in range(len(tag_list)) :
        if i == 0 :
            query['complex'] = Q(tag_searchable__contains=tag_list[i].name)
        else :
            query['complex'] = query['complex'] & Q(tag_searchable__contains=tag_list[i].name)
    return query

def _get_criteria_status(query, status_list) :
    status_id_list = get_id_list_from_url(status_list)
    if len(status_id_list) == 0 :
        return query
    query['status__in'] = status_id_list
    return query

def _get_criteria_sort(query, sort_type, sort_order) :
    query_str = "%s%s"
    asc = ""
    if sort_type == "1" :
        asc = "-"

    if sort_order == "1" : # update_date
        query['order_by'] = (query_str % (asc, "update_date"),)
    elif sort_order == "2" : #id
        query['order_by'] = (query_str % (asc, "id"),)
    elif sort_order == "3" : #status
        query['order_by'] = (query_str % (asc, "status"),)
    elif sort_order == "4" : #estimate
        query['order_by'] = (query_str % (asc, "estimate"),)

    return query

def _get_task_bean_list(task_list) :
    task_bean_list = []
    task_id_list = []
    for task in task_list :
        task_id_list.append(task.id)
    if len(task_id_list) > 0 :
        query = {}
        query['task__id__in'] = task_id_list
        #query['select_related'] = True
        #query['order_by'] = ['task_id']
        task_taglist_list = TagList.objects.filter(**query).order_by('task_id').select_related()
        for task in task_list :
            lock_on = False
            task_tag_list = []
            for taglist in task_taglist_list :
                if lock_on == True :
                    if task.id != taglist.task_id :
                        break
                if task.id == taglist.task_id :
                    lock_on = True
                    task_tag_list.append(taglist.tag)
            task_bean_list.append(TaskBean( task.id, task.task, task.create_date, task.update_date, task.estimate, task.status, task_tag_list))
    return task_bean_list

def update_status(request, task_id, status):
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404
    task.status = status
    task.update_date = datetime.now()
    task.save()

    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % task.id)

def delete(request, task_id) :
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404
    task.delete()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/TaskList/')

def add_tag(request, task_id, tag_id):
    try :
        tsk = Task.objects.get(pk=task_id)
        tg  = Tag.objects.get(pk=tag_id)
    except Task.DoesNotExist :
        raise Http404
    except Tag.DoesNotExist :
        raise Http404
    taglist = TagList(task=tsk, tag=tg)
    taglist.save()
    recreateTask(task_id)
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % tsk.id)

def remove_tag(request, task_id, tag_id):
    try :
        taglist = TagList.objects.get(task__id__exact=task_id, tag__id__exact=tag_id)
    except TagList.DoesNotExist :
        raise Http404

    taglist.delete()
    recreateTask(task_id)
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % task_id)

def create_task(request) :
    manipulator = TaskManipulator()
    if request.POST :
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors :
            return add_task(request)
    else :
        errors = {}
        new_data = {'status': "3"}
    form = forms.FormWrapper(manipulator, new_data, errors)
    status_list = getStatusList()
    tag_list = Tag.objects.filter(visible__exact=True)
    return render_to_response('workstyle/TaskFormNew',{ 'form': form, 'tag_list': tag_list,'status_list': status_list, 'workstyle_root': WORKSTYLE_ROOT })

def add_task(request):
    in_status = request.POST["status"]
    in_task_body = request.POST['task']
    in_estimate = request.POST['estimate']
    if in_estimate == "" :
        in_estimate = 0
    try :
        in_file = request.FILES['attachFile']
    except MultiValueDictKeyError :
        in_file = None
    in_task_tag = request.POST['task_tag']

    in_comment_body = request.POST['comment']
    in_commentator = request.POST['commentator']

    task = Task(task=in_task_body, estimate=in_estimate, status=in_status, update_date=datetime.now())
    task.save()
    task_id = task.id

    if in_file :
        in_file_name = in_file['filename']
        in_content = in_file['content']
        attachment = Attachment(name=in_file_name, size=1, task=task, create_date=datetime.now())
        attachment.save_file_file(filename=in_file_name, raw_contents=in_content)
        attachment.save()

    if in_comment_body :
        task.comment_set.add(comment=in_comment_body, commentator=in_commentator)

    in_task_tag_candidate_list_tmp = string.split(in_task_tag, "]")
    in_task_tag_candidate_list = []
    for in_task_tag_candidate in in_task_tag_candidate_list_tmp :
        in_task_tag_candidate_list.append(string.strip(string.replace(in_task_tag_candidate, "[", "")))

    current_taglist_list = task.taglist_set.all()
    for taglist in current_taglist_list:
        taglist.delete()

    for tag_candidate in in_task_tag_candidate_list :
        if tag_candidate != "":
            try :
                tag = Tag.objects.get(name__exact=tag_candidate)
            except Tag.DoesNotExist :
                tag = Tag(name=tag_candidate)
                tag.save()
            taglist = TagList(task=task, tag=tag)
            taglist.save()
    recreateTask(task_id=task.id)
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % task_id)

def edit_task(request, task_id) :
    manipulator = TaskManipulator()
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404

    if request.POST :
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors :
            return update_task(request, task_id)
    else :
        errors = {}
        new_data = {'status': str(task.status), 'task': task.task, 'estimate': task.estimate, 'comment': '', 'commentator': ''}

    form = forms.FormWrapper(manipulator, new_data, errors)

    tag_list = Tag.objects.filter(visible__exact=True)
    status_list = getStatusList()

    task_taglist_list = task.taglist_set.select_related()
    task_tag_list = []
    for taglist in task_taglist_list:
        task_tag_list.append(taglist.tag)

    tag_with_selected_list = []
    for tag in tag_list :
        tag_with_selected = TaskTag(tag.id, tag.name, tag.tag_type, tag.visible)
        tag_with_selected_list.append(tag_with_selected)
        for task_tag in task_tag_list :
            if tag.id == task_tag.id :
                tag_with_selected.selected = True

    return render_to_response('workstyle/TaskFormEdit',{'form': form, 'task': task, 'tag_list': tag_list,'status_list': status_list, 'task_tag_list': task_tag_list, 'tag_with_selected_list': tag_with_selected_list, 'workstyle_root': WORKSTYLE_ROOT })

def update_task(request, task_id):
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404

    in_status = request.POST["status"]
    in_task_body = request.POST['task']
    in_estimate = request.POST['estimate']
    try :
        in_file = request.FILES['attachFile']
    except MultiValueDictKeyError :
        in_file = None
    in_task_tag = request.POST['task_tag']

    in_comment_body = request.POST['comment']
    in_commentator = request.POST['commentator']

    task.status = in_status
    task.task = in_task_body
    task.estimate = in_estimate
    task.update_date = datetime.now()
    task.save()

    if in_file :
        in_file_name = in_file['filename']
        in_content = in_file['content']
        attachment = Attachment(name=in_file_name, size=1, task=task, create_date=datetime.now())
        attachment.save_file_file(filename=in_file_name, raw_contents=in_content)
        attachment.save()

    if in_comment_body :
        c = Comment(comment=in_comment_body, commentator=in_commentator)
        c.task = task
        c.save()

    in_task_tag_candidate_list_tmp = string.split(in_task_tag, "]")
    in_task_tag_candidate_list = []
    for in_task_tag_candidate in in_task_tag_candidate_list_tmp :
        in_task_tag_candidate_list.append(string.strip(string.replace(in_task_tag_candidate, "[", "")))

    current_taglist_list = task.taglist_set.all()
    for taglist in current_taglist_list:
        taglist.delete()

    for tag_candidate in in_task_tag_candidate_list :
        if tag_candidate != "":
            try :
                tag = Tag.objects.get(name__exact=tag_candidate)
            except Tag.DoesNotExist :
                tag = Tag(name=tag_candidate)
                tag.save()
            taglist = TagList(task=task, tag=tag)
            taglist.save()

    recreateTask(task_id=task.id)
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % task_id)

def attachment_delete(request, task_id, attachment_id):
    try :
        attach = Attachment.objects.get(pk=attachment_id)
    except Attachment.DoesNotExist :
        raise Http404
    attach.delete()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Task/%s/' % task_id)

class TaskTag :
    id = 0
    name = ""
    tag_type = 0
    visible = True
    selected = False
    def __init__(self, id, name, tag_type, visible):
        self.id = id
        self.name = name
        self.tag_type = tag_type
        self.visible = visible

class TaskBean :
    id = 0
    task = ""
    create_date = None
    update_date = None
    estimate = 0
    status = 3
    tag_list = []
    def __init__(self, id, task, create_date, update_date, estimate, status, tag_list) :
        self.id = id
        self.task = task
        self.create_date = create_date
        self.update_date = update_date
        self.status = status
        self.tag_list = tag_list
        if estimate != "" :
            self.estimate = estimate
