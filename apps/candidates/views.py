
from datetime import datetime, time, timedelta
import os
import uuid

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


# -----------------------------------------
# Candidate Profile CRUD API
# -----------------------------------------

class CandidateProfileAPIView(generics.GenericAPIView):

    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role not in ["CANDIDATE", "ADMIN"]:
            raise PermissionDenied(
                "Only candidates and admins can access candidate profiles."
            )

        if user.role == "ADMIN":
            profile_id = self.request.query_params.get("id")

            if profile_id:
                return get_object_or_404(
                    CandidateProfile.objects.select_related("user"),
                    id=profile_id,
                    is_deleted=False
                )

        return get_object_or_404(
            CandidateProfile.objects.select_related("user"),
            user=user,
            is_deleted=False
        )

    def get(self, request):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def post(self, request):

        if request.user.role != "CANDIDATE":
            raise PermissionDenied(
                "Only candidates can create candidate profiles."
            )

        if CandidateProfile.objects.filter(user=request.user).exists():
            raise PermissionDenied(
                "Candidate profile already exists."
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        return self.update_profile(request, partial=False)

    def patch(self, request):
        return self.update_profile(request, partial=True)

    def update_profile(self, request, partial):

        profile = self.get_object()

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):

        profile = self.get_object()
        profile.is_deleted = True
        profile.save(update_fields=["is_deleted", "updated_at"])

        return Response(
            {"message": "Candidate profile deleted successfully."}
        )


# -----------------------------------------
# Candidate Profile Pagination
# -----------------------------------------

class CandidateProfilePagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -----------------------------------------
# Paginated Candidate List + Search + Filters
# -----------------------------------------

class CandidateProfileListAPIView(generics.ListAPIView):

    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CandidateProfilePagination

    def get_queryset(self):

        user = self.request.user

        # Role-based access
        if user.role == "ADMIN":

            queryset = CandidateProfile.objects.select_related(
                "user"
            ).all()

        elif user.role == "CANDIDATE":

            queryset = CandidateProfile.objects.select_related(
                "user"
            ).filter(
                user=user,
                is_deleted=False
            )

        else:
            raise PermissionDenied(
                "Only candidates and admins can access candidate profiles."
            )

        # ---------------------------------
        # 1. Keyword Search
        # ---------------------------------

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(skills__icontains=search) |
                Q(education__icontains=search) |
                Q(experience__icontains=search)
            )

        # ---------------------------------
        # 2. Role Filter
        # ---------------------------------

        role = self.request.query_params.get("role")

        if role:
            queryset = queryset.filter(
                user__role__iexact=role
            )

        # ---------------------------------
        # 3. Optimized Date Filter
        # ---------------------------------

        date = self.request.query_params.get("date")

        if date:

            parsed_date = parse_date(date)

            if parsed_date is None:
                raise ValidationError({
                    "date": "Use YYYY-MM-DD format."
                })

            start_datetime = timezone.make_aware(
                datetime.combine(parsed_date, time.min)
            )

            end_datetime = start_datetime + timedelta(days=1)

            queryset = queryset.filter(
                created_at__gte=start_datetime,
                created_at__lt=end_datetime
            )

        # ---------------------------------
        # 4. Status Filter
        # ---------------------------------

        status_filter = self.request.query_params.get("status")

        if status_filter:

            status_value = status_filter.lower()

            if status_value == "active":

                queryset = queryset.filter(
                    is_deleted=False
                )

            elif status_value == "deleted":

                if user.role != "ADMIN":
                    raise PermissionDenied(
                        "Only admins can view deleted profiles."
                    )

                queryset = queryset.filter(
                    is_deleted=True
                )

            else:
                raise ValidationError({
                    "status": "Use active or deleted."
                })

        else:
            # Show active profiles by default
            queryset = queryset.filter(
                is_deleted=False
            )

        return queryset.order_by("id")


# -----------------------------------------
# Resume Upload API
# -----------------------------------------

class ResumeUploadAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        if request.user.role != "CANDIDATE":
            raise PermissionDenied(
                "Only candidates can upload resumes."
            )

        profile = get_object_or_404(
            CandidateProfile,
            user=request.user,
            is_deleted=False
        )

        uploaded_file = request.FILES.get("resume")

        if not uploaded_file:
            raise ValidationError(
                {"resume": "Please upload a resume file."}
            )

        # File size validation (5 MB)
        if uploaded_file.size > 5 * 1024 * 1024:
            raise ValidationError(
                {"resume": "File size must not exceed 5 MB."}
            )

        # File extension validation
        extension = os.path.splitext(uploaded_file.name)[1].lower()

        allowed_extensions = [".pdf", ".doc", ".docx"]

        if extension not in allowed_extensions:
            raise ValidationError(
                {"resume": "Only PDF, DOC and DOCX files are allowed."}
            )

        # Basic file signature validation
        uploaded_file.seek(0)
        file_header = uploaded_file.read(8)
        uploaded_file.seek(0)

        if extension == ".pdf" and not file_header.startswith(b"%PDF-"):
            raise ValidationError(
                {"resume": "Invalid PDF file."}
            )

        if extension == ".doc" and not file_header.startswith(
            bytes.fromhex("D0CF11E0A1B11AE1")
        ):
            raise ValidationError(
                {"resume": "Invalid DOC file."}
            )

        if extension == ".docx" and not file_header.startswith(b"PK"):
            raise ValidationError(
                {"resume": "Invalid DOCX file."}
            )

        # Generate unique filename
        uploaded_file.name = f"{uuid.uuid4().hex}{extension}"

        profile.resume = uploaded_file
        profile.save(update_fields=["resume", "updated_at"])

        return Response(
            {
                "message": "Resume uploaded successfully.",
                "resume": profile.resume.name
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------------------
# Resume Download API
# -----------------------------------------

class ResumeDownloadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role not in ["CANDIDATE", "ADMIN"]:
            raise PermissionDenied(
                "Only candidates and admins can download resumes."
            )

        # Candidate can download own resume
        if user.role == "CANDIDATE":

            profile = get_object_or_404(
                CandidateProfile,
                user=user,
                is_deleted=False
            )

        # Admin must provide candidate ID
        else:

            candidate_id = request.query_params.get("candidate_id")

            if not candidate_id:
                raise ValidationError(
                    {"candidate_id": "Please provide a candidate ID."}
                )

            profile = get_object_or_404(
                CandidateProfile,
                id=candidate_id,
                is_deleted=False
            )

        if not profile.resume:
            raise ValidationError(
                {"resume": "No resume uploaded."}
            )

        if not profile.resume.storage.exists(profile.resume.name):
            raise ValidationError(
                {"resume": "Resume file not found in storage."}
            )

        return FileResponse(
            profile.resume.open("rb"),
            as_attachment=True,
            filename=os.path.basename(profile.resume.name)
        )
