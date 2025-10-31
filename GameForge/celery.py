from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameForge.settings')
app = Celery('GameForge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks('tasks')

from celery import chain
from tasks.generate_universe import generate_universe
from tasks.generate_scenario import generate_scenario
from tasks.generate_characters import generate_characters
from tasks.generate_char_img import generate_char_img
from tasks.generate_locations import generate_locations

workflow = chain(
    generate_universe.s(),
    generate_scenario.s(),
    generate_characters.s(),
    generate_char_img.s(),
    generate_locations.s()
)
workflow.apply_async()