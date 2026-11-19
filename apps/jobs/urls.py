
from django.urls import path

from .views import (
    EmployerJobCreateAPIView,
    JobUpdateAPIView,
    JobStatusUpdateAPIView,
    ActiveJobListAPIView,
    FeaturedJobListAPIView,
    LatestJobListAPIView,
)

urlpatterns = [
    # Existing APIs
    path('create/', EmployerJobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/update/', JobUpdateAPIView.as_view(), name='job-update'),
    path('<int:pk>/status/', JobStatusUpdateAPIView.as_view(), name='job-status'),

    # Day 17 Public Job Listing APIs
    path('list/', ActiveJobListAPIView.as_view(), name='active-job-list'),
    path('featured/', FeaturedJobListAPIView.as_view(), name='featured-jobs'),
    path('latest/', LatestJobListAPIView.as_view(), name='latest-jobs'),
]
