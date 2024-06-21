import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Social_Media_Demo.settings")
app = Celery("Social_Media_Demo")
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
                            'Send_mail_to_Client': {
                                                        'task': 'Social_Media_App.task.send_mail',
                                                        'schedule': 30.0, #every 30 seconds it will be called
                                                        #'args': (2,) you can pass arguments also if rquired
                                                    }
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')