from celery.result import AsyncResult
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rank_analysis.celery_services.celery_tasks.celery_tasks import (
    get_google_ranking_celery,
)
from rank_analysis.common.constants import TASK_PENDING, RESULTS_NOT_AVAILABLE
from rank_analysis.serializers import (
    SearchRequestSerializer,
    SearchResponseSerializer,
    TaskResultResponseSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class SearchViewSet(ModelViewSet):
    @swagger_auto_schema(
        request_body=SearchRequestSerializer,
        responses={201: SearchResponseSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """
        Create a task asynchronously using Celery worker.

        Parameters:
        - request (url): Single URL.
        - request (invites): List of invites.

        Returns:
        - 201 Accepted: If the task is successfully created.
        """
        data = [{"url": request.data["url"], "keywords": request.data["invites"]}]
        task = get_google_ranking_celery.delay(data)

        return Response({"task_id": task.id, "status": status.HTTP_201_CREATED})


class TaskResultView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "task_id",
                openapi.IN_QUERY,
                description="Task id",
                type=openapi.FORMAT_UUID,
            )
        ],
        responses={201: TaskResultResponseSerializer, 400: "Bad Request"},
    )
    def get(self, request):
        """
        Retrieve the status and result of a task.

        Query Parameters:
        - task_id (str): The unique identifier for the task.

        Returns:
        - 200 OK: If the task information is successfully retrieved.
        - 400 Bad Request: If the task_id is not provided.
        """
        task_id = request.GET.get("task_id")

        if not task_id:
            return Response({"message": "Task ID is required"}, status=400)

        task = AsyncResult(task_id)
        response_data = {"task_id": task_id, "status": task.status}

        if task.ready():
            response_data["result"] = task.result
        elif task.successful():
            response_data["result"] = TASK_PENDING
        else:
            response_data["result"] = RESULTS_NOT_AVAILABLE

        return Response(response_data)
