from django.conf.urls.defaults import *
#from django.views.generic.create_update import *
#from django.views.generic.list_detail import *

from workstyle.ws.models import *

info_dict = {'queryset': Task.objects.all().order_by("create_date"),}

urlpatterns = patterns('',
    (r'^$','django.views.generic.list_detail.object_list',{'queryset': Task.objects.all().order_by("create_date"),'allow_empty': True}),
    (r'^task/add/$', 'django.views.generic.create_update.create_object',{'model': Task}),
    (r'^task/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',info_dict),
    (r'^task/(?P<object_id>\d+)/contents/update/$', 'workstyle.ws.views.update_contents'),
    (r'^task/(?P<object_id>\d+)/priority/update/$', 'workstyle.ws.views.update_priority'),
    (r'^task/(?P<object_id>\d+)/tag/update/$', 'workstyle.ws.views.update_tag'),
    (r'^static/resources/local.js$', 'django.views.generic.simple.direct_to_template',{'template': 'local.js'}),
    (r'^tag/$', 'django.views.generic.list_detail.object_list',{'queryset': Tag.objects.all().order_by("name"),'allow_empty': True}),
    (r'^task/(?P<task_id>\d+)/property/update/$','workstyle.ws.views.update_task_property'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # Uncomment this for admin:
        (r'^admin/', include('django.contrib.admin.urls')),
        
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
