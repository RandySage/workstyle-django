from django.conf.urls.defaults import *
from django.conf import settings
from WorkStyle.workstyle.models import Task

urlpatterns = patterns('',
    # Example:
    # (r'^WorkStyle/', include('WorkStyle.foo.urls.foo')),
    (r'^$', 'WorkStyle.workstyle.views.index'),
    (r'^TaskList/$', 'WorkStyle.workstyle.view.task.list_default'),
    (r'^TaskList/rss/(?P<sort_type>\d+)/(?P<sort_order>\d+)/(?P<status_list>\S+)/(?P<tag_list>\S+)/(?P<offset>\d+)/(?P<limit>\d+)/(?P<key>\S+)/$', 'WorkStyle.workstyle.view.task.list_rss'),
    (r'^TaskList/atom/(?P<sort_type>\d+)/(?P<sort_order>\d+)/(?P<status_list>\S+)/(?P<tag_list>\S+)/(?P<offset>\d+)/(?P<limit>\d+)/(?P<key>\S+)/$', 'WorkStyle.workstyle.view.task.list_atom'),
    (r'^TaskList/(?P<sort_type>\d+)/(?P<sort_order>\d+)/(?P<status_list>\S+)/(?P<tag_list>\S+)/(?P<offset>\d+)/(?P<limit>\d+)/(?P<key>\S+)/$', 'WorkStyle.workstyle.view.task.list'),
    (r'^TaskList/update_status/(?P<task_id>\d+)/(?P<status>\d+)/(?P<sort_type>\d+)/(?P<sort_order>\d+)/(?P<status_list>\S+)/(?P<tag_list>\S+)/(?P<offset>\d+)/(?P<limit>\d+)/(?P<key>\S+)/$', 'WorkStyle.workstyle.view.task.list_update_status'),
    (r'^TaskList/delete_task/(?P<task_id>\d+)/(?P<sort_type>\d+)/(?P<sort_order>\d+)/(?P<status_list>\S+)/(?P<tag_list>\S+)/(?P<offset>\d+)/(?P<limit>\d+)/(?P<key>\S+)/$', 'WorkStyle.workstyle.view.task.list_delete_task'),
    (r'^Task/(?P<task_id>\d+)/$', 'WorkStyle.workstyle.view.task.index'),
    (r'^Task/(?P<task_id>\d+)/update_status/(?P<status>\d+)/$', 'WorkStyle.workstyle.view.task.update_status'),
    (r'^Task/(?P<task_id>\d+)/add_tag/(?P<tag_id>\d+)/$', 'WorkStyle.workstyle.view.task.add_tag'),
    (r'^Task/(?P<task_id>\d+)/remove_tag/(?P<tag_id>\d+)/$', 'WorkStyle.workstyle.view.task.remove_tag'),
    (r'^Task/add/$', 'django.views.generic.create_update.create_object', {'model': Task}),
    (r'^Task/(?P<task_id>\d+)/edit/$', 'WorkStyle.workstyle.view.task.edit_task'),
    (r'^Task/(?P<task_id>\d+)/update/$', 'WorkStyle.workstyle.view.task.edit_task'),
    (r'^Task/(?P<task_id>\d+)/delete/$', 'WorkStyle.workstyle.view.task.delete'),
    (r'^Task/(?P<task_id>\d+)/delete_attachment/(?P<attachment_id>\d+)/$', 'WorkStyle.workstyle.view.task.attachment_delete'),
    (r'^Tag/$', 'WorkStyle.workstyle.view.tag.index'),
    (r'^Tag/(?P<tag_id>\d+)/select_type/(?P<type_id>\d+)/$', 'WorkStyle.workstyle.view.tag.select_type'),
    (r'^Tag/(?P<tag_id>\d+)/switch_visible/(?P<visible_flag>\w+)/$', 'WorkStyle.workstyle.view.tag.switch_visible'),
    (r'^Tag/(?P<tag_id>\d+)/delete/$', 'WorkStyle.workstyle.view.tag.delete'),
    (r'^resources/(?P<path>.*)','django.views.static.serve', {'document_root' : settings.WORKSTYLE_MEDIA_ROOT, 'show_indexes':False}),

    # Uncomment this for admin:
    # (r'^admin/', include('django.contrib.admin.urls.admin')),
)
