from django.conf import settings

def sd_url(request):
    return {'SD_URL': settings.SD_URL}