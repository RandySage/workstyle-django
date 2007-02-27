from workstyle.ws.models import Tag

def workstyle_context(request):
    return {'tag_list': Tag.public_objects.all()}
