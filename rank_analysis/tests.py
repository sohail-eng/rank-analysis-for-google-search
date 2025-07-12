from unittest.mock import patch

from celery.result import AsyncResult
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TaskResultViewTest(TestCase):
    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient.
        """
        self.client = APIClient()

    def test_task_result_view_with_valid_task_id(self):
        """
        Test the TaskResultView with a valid task_id.
        This test checks if the view returns the expected response when
        provided with a valid task_id.
        """
        url = reverse("task-status")
        task_id = "valid_task_id"

        response = self.client.get(url, {"task_id": task_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertIn("task_id", data)
        self.assertIn("status", data)
        self.assertIn("result", data)

    def test_task_result_view_with_invalid_task_id(self):
        """
        Test the TaskResultView with an invalid task_id.
        This test checks if the view returns the expected response when
        not provided with a task_id.
        """
        url = reverse("task-status")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("message", data)


class SearchViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch(
        "rank_analysis.celery_services.celery_tasks.celery_tasks.get_google_ranking_celery.delay"
    )
    def test_create_method_with_valid_data(self, mock_delay):
        # Replace 'your-search-view-url' with the actual URL name or path
        url = reverse("task-status")
        data = [
            {
                "url": "www.gccsolutions.com",
                "invites": ["commercial agent in abu dhabi"],
            }
        ]

        # Mock Celery task delay method
        mock_task = AsyncResult("mocked_task_id")
        mock_delay.return_value = mock_task

        response = self.client.post(url, data, format="json")

        # Assert the response status code and content
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {"task_id": "mocked_task_id", "status": status.HTTP_201_CREATED},
        )

        # Assert that the Celery task was called with the correct data
        mock_delay.assert_called_once_with(
            [
                {
                    "url": "www.gccsolutions.com",
                    "invites": ["commercial agent in abu dhabi"],
                }
            ]
        )

    @patch(
        "rank_analysis.celery_services.celery_tasks.celery_tasks.get_google_ranking_celery.delay"
    )
    def test_create_method_with_invalid_results(self, mock_delay):
        url = reverse("task-status")
        data = [
            {
                "url": "www.gccsolutions.com",
                "invites": ["commercial agent in abu dhabi"],
            }
        ]

        mock_delay.return_value = None
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, {"error": "Unexpected result from Celery task"})
