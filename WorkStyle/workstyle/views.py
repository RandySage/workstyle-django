import urllib
from WorkStyle.workstyle.models import Task, Tag, Attachment, Comment
from django.views.generic.list_detail import object_list
from django.db.models.query import Q

def index(request) :
    http_query = ''
    selected_tag_list = request.GET.getlist('tag')
    selected_status_list = request.GET.getlist('status')
    order_by = request.GET.get('order_by', None)
    query_set = Task.objects.all()

    if selected_tag_list :
        for i, tag in enumerate(selected_tag_list) :
            http_query = http_query + ('&tag=%s' % urllib.quote(tag))
            if i == 0:
                q = Q(tag_searchable__icontains=tag)
            else :
                q = q & Q(tag_searchable__icontains=tag)
        query_set.filter(q)
    if selected_status_list :
        for i, status in enumerate(selected_status_list) :
            http_query = http_query + '&status=%s' % urllib.quote(status)
            if i == 0:
                q = Q(status_exact=status)
            else :
                q = q | Q(status_exact=status)
        query_set.filter(q)
    valid_order_by = ('status', '-status', 'id', '-id', 'estimate', '-estimate', 'update_date', '-update_date')
    if order_by in valid_order_by:
        http_query = http_query + '&order_by=%s' % urllib.quote(order_by)
        query_set.order_by(order_by)
    return object_list(request, query_set, paginate_by=20, allow_empty=True, extra_context={'http_query': http_query})
