"""
WSGI config for KitsuneCore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables
load_dotenv()

application_name = os.getenv('APP_NAME')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{application_name}.settings')

application = get_wsgi_application()
