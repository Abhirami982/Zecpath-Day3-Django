
from pathlib import Path

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.candidates.models import CandidateProfile
from apps.jobs.models import Job
from apps.employers.models import EmployerProfile
from .models import Application


class ApplyJobAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Candidate-only access
        if request.user.role != "CANDIDATE":
            return Response(
                {"error": "Only candidates can apply for jobs."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get candidate profile
        candidate = get_object_or_404(
            CandidateProfile,
            user=request.user,
            is_deleted=False
        )

        # Get job ID
        job_id = request.data.get("job_id")

        if not job_id:
            return Response(
                {"error": "Job ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check job existence
        job = get_object_or_404(Job, id=job_id)

        # Check job status
        if job.status != "ACTIVE":
            return Response(
                {"error": "This job is not active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent duplicate applications
        if Application.objects.filter(
            candidate=candidate,
            job=job
        ).exists():
            return Response(
                {"error": "You have already applied for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check candidate resume
        if not candidate.resume:
            return Response(
                {"error": "Please upload your resume before applying."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Copy resume snapshot
        candidate.resume.open("rb")
        resume_content = candidate.resume.read()
        original_name = Path(candidate.resume.name).name
        candidate.resume.close()

        application = Application(
            candidate=candidate,
            job=job,
            status="APPLIED"
        )

        application.resume_snapshot.save(
            f"candidate_{candidate.id}_job_{job.id}_{original_name}",
            ContentFile(resume_content),
            save=False
        )

        application.save()

        return Response(
            {
                "success": True,
                "message": "Job application submitted successfully.",
                "application_id": application.id,
                "job_id": job.id,
                "status": application.status,
                "applied_at": application.applied_at
            },
            status=status.HTTP_201_CREATED
        )


class ApplicationHistoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "CANDIDATE":
            return Response(
                {"error": "Only candidates can view application history."},
                status=status.HTTP_403_FORBIDDEN
            )

        candidate = get_object_or_404(
            CandidateProfile,
            user=request.user,
            is_deleted=False
        )

        applications = Application.objects.filter(
            candidate=candidate
        ).select_related("job").order_by("-applied_at")

        data = []

        for application in applications:
            data.append({
                "application_id": application.id,
                "job_id": application.job.id,
                "job_title": application.job.title,
                "status": application.status,
                "applied_at": application.applied_at
            })

        return Response({
            "success": True,
            "count": len(data),
            "applications": data
        })


class AppliedJobsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "CANDIDATE":
            return Response(
                {"error": "Only candidates can view applied jobs."},
                status=status.HTTP_403_FORBIDDEN
            )

        candidate = get_object_or_404(
            CandidateProfile,
            user=request.user,
            is_deleted=False
        )

        applications = Application.objects.filter(
            candidate=candidate
        ).select_related("job").order_by("-applied_at")

        data = []

        for application in applications:
            data.append({
                "job_id": application.job.id,
                "job_title": application.job.title,
                "application_id": application.id,
                "application_status": application.status,
                "applied_at": application.applied_at
            })

        return Response({
            "success": True,
            "count": len(data),
            "applied_jobs": data
        })


class EmployerApplicationStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # Allowed workflow transitions
    ALLOWED_TRANSITIONS = {
        "APPLIED": ["SHORTLISTED", "REJECTED"],
        "SHORTLISTED": ["INTERVIEW_SCHEDULED", "REJECTED"],
        "INTERVIEW_SCHEDULED": ["SELECTED", "REJECTED"],
        "REJECTED": [],
        "SELECTED": []
    }

    def patch(self, request, application_id):

        # Employer-only access
        if request.user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can update application status."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get employer profile
        employer = get_object_or_404(
            EmployerProfile,
            user=request.user
        )

        # Get application
        application = get_object_or_404(
            Application,
            id=application_id
        )

        # Check job ownership
        if application.job.employer_id != employer.id:
            return Response(
                {
                    "error": "You cannot update applications for another employer's job."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Get new status
        new_status = request.data.get("status")

        # Validate status
        if new_status not in Application.Status.values:
            return Response(
                {"error": "Invalid application status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get current status
        current_status = application.status

        # Check allowed transition
        allowed_statuses = self.ALLOWED_TRANSITIONS.get(
            current_status, []
        )

        if new_status not in allowed_statuses:
            return Response(
                {
                    "error": "Invalid workflow transition.",
                    "current_status": current_status,
                    "allowed_next_statuses": allowed_statuses
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update status
        application.status = new_status
        application.save()

        return Response({
            "success": True,
            "message": "Application status updated successfully.",
            "application_id": application.id,
            "previous_status": current_status,
            "new_status": application.status,
            "updated_at": application.updated_at
        })
