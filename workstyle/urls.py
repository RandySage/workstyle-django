from django.conf.urls.defaults import *
#from django.views.generic.create_update import *
#from django.views.generic.list_detail import *

from workstyle.ws.models import *

info_dict = {'queryset': Task.objects.all().order_by("create_date"),}

urlpatterns = patterns('',
    (r'^$','django.views.generic.list_detail.object_list',{'queryset': Task.objects.all().order_by("create_date"),'allow_empty': True}),
    (r'^task/add/$', 'django.views.generic.create_update.create_object',{'model': Task}),
    (r'^task/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',info_dict),
    (r'^static/resources/local.js$', 'django.views.generic.simple.direct_to_template',{'template': 'local.js'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
