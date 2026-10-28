
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Job
from .serializers import JobSerializer
from services.job_service import get_all_jobs


def home(request):
    """Return the backend welcome message."""
    return HttpResponse("Hello Zecpath Backend")


class JobListAPI(generics.ListAPIView):
    """Provide a list of available jobs."""

    serializer_class = JobSerializer

    def get_queryset(self):
        return get_all_jobs()


class JobCreateAPI(generics.CreateAPIView):
    """Create a new job."""

    queryset = Job.objects.all()
    serializer_class = JobSerializer


@api_view(["GET"])
def user_test_api(request):
    """Check whether the user test API is working."""
    return Response({
        "message": "User Test API is working!",
        "status": "success",
    })
