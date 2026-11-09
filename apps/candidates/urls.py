
from django.urls import path

from .views import (
    CandidateProfileAPIView,
    CandidateProfileListAPIView,
    ResumeUploadAPIView,
    ResumeDownloadAPIView
)

urlpatterns = [

    # Paginated candidate list
    path(
        '',
        CandidateProfileListAPIView.as_view(),
        name='candidate-list'
    ),

    # Candidate profile CRUD
    path(
        'profile/',
        CandidateProfileAPIView.as_view(),
        name='candidate-profile'
    ),

    # Resume upload
    path(
        'resume/upload/',
        ResumeUploadAPIView.as_view(),
        name='resume-upload'
    ),

    # Resume download
    path(
        'resume/download/',
        ResumeDownloadAPIView.as_view(),
        name='resume-download'
    ),
]
