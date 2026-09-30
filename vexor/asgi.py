"""
ASGI config for VEXOR GAMING project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vexor.settings.development')

application = get_asgi_application()