from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booking_system.settings")

# celery instance
app = Celery("booking_system")

# load the task module
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
