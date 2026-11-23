
from django.urls import path

from .views import (
    EmployerJobCreateAPIView,
    JobUpdateAPIView,
    JobStatusUpdateAPIView,
    ActiveJobListAPIView,
    FeaturedJobListAPIView,
    LatestJobListAPIView,
    EmployerDashboardJobListAPIView,
    EmployerDashboardJobUpdateAPIView,
    EmployerDashboardCloseHiringAPIView,
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

    # Day 20 Employer Dashboard APIs
    path('dashboard/jobs/', EmployerDashboardJobListAPIView.as_view(), name='employer-dashboard-jobs'),
    path('dashboard/jobs/<int:pk>/update/', EmployerDashboardJobUpdateAPIView.as_view(), name='employer-dashboard-job-update'),
    path('dashboard/jobs/<int:pk>/close/', EmployerDashboardCloseHiringAPIView.as_view(), name='employer-dashboard-job-close'),
]
