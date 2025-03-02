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
        'APP_LOGO_PATH': settings.APP_INFO['APP_LOGO_PATH'],
        'APP_FAVICON_PATH': settings.APP_INFO['APP_FAVICON_PATH'],
        'APP_LAYOUT_DIRECTION': settings.APP_INFO['APP_LAYOUT_DIRECTION'],
        'APP_LAYOUT_LANGUAGE': settings.APP_INFO['APP_LAYOUT_LANGUAGE'],
        'SOCIAL_LINKS': settings.APP_INFO['SOCIAL_LINKS'],
        
        # Meta information
        'META_AUTHOR': settings.APP_INFO['META_INFO']['META_AUTHOR'],
        'IMAGE_512x512_PATH': settings.APP_INFO['META_INFO']['IMAGE_512x512_PATH'],
        'IMAGE_180x180_PATH': settings.APP_INFO['META_INFO']['IMAGE_180x180_PATH'],
        'IMAGE_70x70_PATH': settings.APP_INFO['META_INFO']['IMAGE_70x70_PATH'],
        'IMAGE_32x32_PATH': settings.APP_INFO['META_INFO']['IMAGE_32x32_PATH'],
        'IMAGE_16x16_PATH': settings.APP_INFO['META_INFO']['IMAGE_16x16_PATH'],
        'SVG_PATH': settings.APP_INFO['META_INFO']['SVG_PATH'],
        
        # Page meta information - making these default values that can be overridden
        'PAGE_META': {
            'PAGE_TITLE': settings.APP_INFO['PAGE_META_INFO']['PAGE_TITLE'],
            'META_DESCRIPTION': settings.APP_INFO['PAGE_META_INFO']['META_DESCRIPTION'],
            'META_KEYWORDS': settings.APP_INFO['PAGE_META_INFO']['META_KEYWORDS'],
            'CANONICAL_URL': settings.APP_INFO['PAGE_META_INFO']['CANONICAL_URL'],
            'ROBOTS_CONTENT': settings.APP_INFO['PAGE_META_INFO']['ROBOTS_CONTENT'],
            'OG_IMAGE_1080x1080_PATH': settings.APP_INFO['PAGE_META_INFO']['OG_IMAGE_1080x1080_PATH'],
        },
    }
    
    return context
