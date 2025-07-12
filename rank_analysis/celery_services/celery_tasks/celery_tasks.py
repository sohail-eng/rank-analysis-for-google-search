import logging
from typing import Dict

from rank_analysis.celery_services.celery_services import celery_app
from rank_analysis.google_rank.main import google_rank

logger = logging.getLogger(__name__)


@celery_app.task
def get_google_ranking_celery(data: Dict):
    results = google_rank(data)
    return results
