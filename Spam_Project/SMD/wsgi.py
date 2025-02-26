import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables from .env file
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMD.settings')

application = get_wsgi_application()

