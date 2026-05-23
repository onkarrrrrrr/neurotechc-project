import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neurotechc.settings")

# Run collectstatic to Vercel's /tmp on startup
if os.environ.get('VERCEL') == '1':
    from django.core.management import call_command
    try:
        call_command('collectstatic', '--noinput')
    except Exception as e:
        print("Startup collectstatic error:", e)

app = get_wsgi_application()
