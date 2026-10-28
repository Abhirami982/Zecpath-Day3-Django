
from .serializers import JobSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http import HttpResponse

from services.job_service import get_all_jobs


def home(request):
    return HttpResponse("Hello Zecpath Backend")


# 1. Job List API
class JobListAPI(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return get_all_jobs()


# 2. Job Create API
class JobCreateAPI(generics.CreateAPIView):
    serializer_class = JobSerializer
    queryset = JobSerializer.Meta.model.objects.all()


# 3. User Test API
@api_view(['GET'])
def user_test_api(request):
    return Response({
        "message": "User Test API is working!",
        "status": "success"
    })
