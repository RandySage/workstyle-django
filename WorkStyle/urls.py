from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^WorkStyle/', include('WorkStyle.workstyle.urls')),

    # Uncomment this for admin:
    # (r'^admin/', include('django.contrib.admin.urls.admin')),
)
