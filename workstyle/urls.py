from django.conf.urls.defaults import *
from django.views.generic.create_update import *

from workstyle.ws.models import *


urlpatterns = patterns('',
    (r'^task/add/$', create_object(model=Task))
)