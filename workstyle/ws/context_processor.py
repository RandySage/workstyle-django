from django.conf import settings
from workstyle.ws.models import Tag

def workstyle_context(request):
    return {'MEDIA_URL': settings.MEDIA_URL,
            'tag_list': Tag.public_objects.all()}
