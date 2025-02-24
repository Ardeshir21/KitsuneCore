from django.conf import settings

def core(request):
    """
    Core context processor that provides common context variables to all templates.
    Reads configuration from settings.py which gets values from environment variables.
    """
    context = {
        # Built-in settings
        'SITE_URL': settings.SITE_URL,
        'DEBUG': settings.DEBUG,
        'MAINTENANCE_MODE': settings.MAINTENANCE_MODE,
        'SUPPORT_EMAIL': settings.EMAIL_HOST_USER,
        
        # App information from settings
        'APP_NAME': settings.APP_INFO['APP_NAME'],
        'COMPANY_NAME': settings.APP_INFO['COMPANY_NAME'],
        'SOCIAL_LINKS': settings.APP_INFO['SOCIAL_LINKS'],
    }
    
    return context
