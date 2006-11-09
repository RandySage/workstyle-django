def server_path(request): 
    from django.conf import settings 
    return {'media_url': settings.MEDIA_URL, 'workstyle_root': settings.WORKSTYLE_ROOT}