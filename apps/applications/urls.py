
from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    AppliedJobsAPIView,
)

urlpatterns = [
    path("apply/", ApplyJobAPIView.as_view(), name="apply-job"),

    path(
        "history/",
        ApplicationHistoryAPIView.as_view(),
        name="application-history"
    ),

    path(
        "applied-jobs/",
        AppliedJobsAPIView.as_view(),
        name="applied-jobs"
    ),
]
