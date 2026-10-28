from .serializers import JobSerializer
from .models import Job
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello Zecpath Backend")


# Existing home view
def home(request):
    return HttpResponse("Hello Zecpath Backend")


# 1. Job List API
class JobListAPI(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# 2. Job Create API
class JobCreateAPI(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# 3. User Test API
@api_view(['GET'])
def user_test_api(request):
    return Response({
        "message": "User Test API is working!",
        "status": "success"
    })
