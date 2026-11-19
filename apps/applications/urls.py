from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    AppliedJobsAPIView,
    EmployerApplicationStatusAPIView,
)

urlpatterns = [
    path(
        "apply/",
        ApplyJobAPIView.as_view(),
        name="apply-job"
    ),

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

    path(
        "<int:application_id>/status/",
        EmployerApplicationStatusAPIView.as_view(),
        name="employer-application-status"
    ),
]
