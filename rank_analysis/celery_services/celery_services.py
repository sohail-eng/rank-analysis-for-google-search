from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from rank_analysis_for_google_search.settings import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rank_analysis_for_google_search.settings")

celery_app = Celery(
    "rank_analysis",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "rank_analysis.celery_services.celery_tasks.celery_tasks",
        "rank_analysis.google_rank.main",
    ],
    task_serializer="json",
    result_serializer="json",
    worker_send_task_events=True,
    task_send_sent_event=True,
)

celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.conf.enable_utc = False

celery_app.autodiscover_tasks()
