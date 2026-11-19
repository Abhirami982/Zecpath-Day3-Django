
import re

from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.employers.models import EmployerProfile
from .models import Job
from .serializers import (
    JobSerializer,
    JobStatusSerializer,
    PublicJobSerializer
)
from .permissions import IsEmployer, IsEmployerOrAdmin


def get_numeric_range(value):
    """Extract numeric values from experience or salary text."""
    numbers = re.findall(r'\d+(?:\.\d+)?', str(value))

    if not numbers:
        return None

    numbers = [float(number) for number in numbers]

    if len(numbers) == 1:
        return numbers[0], numbers[0]

    return min(numbers), max(numbers)


# Reusable optimized queryset for public job listings
def optimized_public_jobs():
    return Job.objects.select_related(
        'employer'
    ).only(
        'id',
        'employer',
        'employer__id',
        'title',
        'description',
        'skills',
        'experience',
        'salary_range',
        'location',
        'job_type',
        'status',
        'is_featured',
        'created_at',
        'updated_at'
    )


class EmployerJobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        employer = EmployerProfile.objects.filter(
            user=self.request.user,
            is_deleted=False
        ).first()

        if not employer:
            raise PermissionDenied(
                "Employer profile not found or inactive."
            )

        serializer.save(employer=employer)


class JobUpdateAPIView(generics.UpdateAPIView):
    queryset = Job.objects.select_related('employer').all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]


class JobStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Job.objects.select_related('employer').all()
    serializer_class = JobStatusSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdmin]


class ActiveJobListAPIView(generics.ListAPIView):
    serializer_class = PublicJobSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params

        jobs = optimized_public_jobs().filter(
            status='ACTIVE'
        ).order_by('-created_at')

        # 1. Keyword search
        keyword = params.get('search') or params.get('keyword')

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(skills__icontains=keyword) |
                Q(location__icontains=keyword)
            )

        # 2. Skill filter
        skill = params.get('skill')

        if skill:
            jobs = jobs.filter(skills__icontains=skill)

        # 3. Location filter
        location = params.get('location')

        if location:
            jobs = jobs.filter(location__icontains=location)

        # 4. Job type filter
        job_type = params.get('job_type')

        if job_type:
            jobs = jobs.filter(job_type=job_type.upper())

        # 5. Experience and salary filters
        min_exp = params.get('min_experience')
        max_exp = params.get('max_experience')

        min_salary = params.get('min_salary')
        max_salary = params.get('max_salary')

        range_filters = (
            min_exp or max_exp or min_salary or max_salary
        )

        if range_filters:
            filtered_jobs = []

            for job in jobs.iterator():
                experience = get_numeric_range(job.experience)
                salary = get_numeric_range(job.salary_range)

                # Experience validation
                if min_exp or max_exp:
                    if experience is None:
                        continue

                    if min_exp and experience[1] < float(min_exp):
                        continue

                    if max_exp and experience[0] > float(max_exp):
                        continue

                # Salary validation
                if min_salary or max_salary:
                    if salary is None:
                        continue

                    if min_salary and salary[1] < float(min_salary):
                        continue

                    if max_salary and salary[0] > float(max_salary):
                        continue

                filtered_jobs.append(job)

            return filtered_jobs

        return jobs


class FeaturedJobListAPIView(generics.ListAPIView):
    serializer_class = PublicJobSerializer
    permission_classes = []

    def get_queryset(self):
        return optimized_public_jobs().filter(
            status='ACTIVE',
            is_featured=True
        ).order_by('-created_at')


class LatestJobListAPIView(generics.ListAPIView):
    serializer_class = PublicJobSerializer
    permission_classes = []

    def get_queryset(self):
        return optimized_public_jobs().filter(
            status='ACTIVE'
        ).order_by('-created_at')[:10]
