from django.urls import path
from .views import (
    CandidateProfileAPIView,
    ResumeUploadAPIView,
    ResumeDownloadAPIView
)

urlpatterns = [
    path(
        'profile/',
        CandidateProfileAPIView.as_view(),
        name='candidate-profile'
    ),

    path(
        'resume/upload/',
        ResumeUploadAPIView.as_view(),
        name='resume-upload'
    ),

    path(
        'resume/download/',
        ResumeDownloadAPIView.as_view(),
        name='resume-download'
    ),
]