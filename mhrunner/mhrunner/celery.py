from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите модуль настроек Django по умолчанию для celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhrunner.settings')

app = Celery('mhrunner')

# Здесь вы можете загрузить конфигурацию celery из конфигурационного файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
