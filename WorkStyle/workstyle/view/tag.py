from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from WorkStyle.workstyle.models import Tag, TagList, Task, TAG_TYPE_CHOICES, TASK_STATUS
from WorkStyle.settings import WORKSTYLE_ROOT

def index(request):
    tag_list = Tag.objects.all()
    tag_type = getTagTypeList()

    return render_to_response('workstyle/TagList', {'tag_list': tag_list, 'tag_type': tag_type, 'workstyle_root': WORKSTYLE_ROOT })

def select_type(request, tag_id, type_id):
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist :
        raise Http404
    tag.tag_type = type_id
    tag.save()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Tag/')

def switch_visible(request, tag_id, visible_flag):
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist :
        raise Http404
    if visible_flag == 'on' :
        tag.visible = True
    else :
        tag.visible = False
    tag.save()
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Tag/')

def delete(request, tag_id):
    try:
        tag = Tag.objects.get(pk=tag_id)
    except Tag.DoesNotExist :
        raise Http404
    taglist_list = tag.taglist_set.all()
    tag.delete()

    task_id_list = ""
    for taglist in taglist_list :
        task_id_list += "%d," % taglist.task_id
    if task_id_list != "" :
        task_id_list = task_id_list.rstrip(",")
        task_list = Task.objects.filter(id__in=[task_id_list])
        for task in task_list :
            recreateTask(task.id)
    return HttpResponseRedirect(WORKSTYLE_ROOT + '/Tag/')


def getStatusList():
    status_list = []
    for task_status in TASK_STATUS:
        status_list.append(TaskStatus(task_status[0], task_status[1], task_status[2]))
    return status_list

def getTagTypeList():
    tag_type = []
    for type in TAG_TYPE_CHOICES:
        tag_type.append(TagType(type[0], type[1]))
    return tag_type

def recreateTask(task_id) :
    try :
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist :
        raise Http404
    task_tag_list = task.taglist_set.select_related()
    searchable_tag = ""
    for task_tag in task_tag_list :
        t = task_tag.tag
        searchable_tag += "	%s" % t.name
    task.tag_searchable = searchable_tag
    task.save()



class TagType:
    id=0
    name=""
    def __init__(self, id, name):
        self.id = id
        self.name = name

class TaskStatus:
    id=0
    name=""
    icon=""
    selected = False
    id_str = ""
    def __init__(self, id, name, icon):
        self.id = id
        self.name = name
        self.icon = icon
        self.id_str = str(self.id)
