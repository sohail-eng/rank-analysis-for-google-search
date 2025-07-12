from django.urls import path
from rank_analysis.views import SearchViewSet, TaskResultView

urlpatterns = [
    path(
        "rank_analysis/",
        SearchViewSet.as_view(
            {
                "post": "create",
            }
        ),
        name="rank-analysis",
    ),
    path("task-status/", TaskResultView.as_view(), name="task-status"),
]
