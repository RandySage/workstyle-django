from django.conf.urls.defaults import *
#from django.views.generic.create_update import *
#from django.views.generic.list_detail import *

from workstyle.ws.models import *

info_dict = {'queryset': Task.objects.all().order_by("create_date"),}

urlpatterns = patterns('',
    (r'^$','django.views.generic.list_detail.object_list',info_dict),
    (r'^task/add/$', 'django.views.generic.create_update.create_object',{'model': Task}),
    (r'^task/$', 'django.views.generic.list_detail.object_detail',dict(info_dict,object_id=1)),
)