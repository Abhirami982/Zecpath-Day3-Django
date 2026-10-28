
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]


urlpatterns = [
    path('', views.home, name='home'),

    # Job List API
    path('jobs/', views.JobListAPI.as_view(), name='job-list'),

    # Job Create API
    path('jobs/create/', views.JobCreateAPI.as_view(), name='job-create'),

    # User Test API
    path('user-test/', views.user_test_api, name='user-test'),
]
