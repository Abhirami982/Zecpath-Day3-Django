from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
import os

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


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
                    CandidateProfile,
                    id=profile_id,
                    is_deleted=False
                )

        return get_object_or_404(
            CandidateProfile,
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

        return Response(serializer.data, status=201)

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
        profile.save()

        return Response(
            {"message": "Candidate profile deleted successfully."}
        )


class ResumeUploadAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        # Allow only candidates
        if request.user.role != "CANDIDATE":
            raise PermissionDenied(
                "Only candidates can upload resumes."
            )

        # Get candidate profile
        profile = get_object_or_404(
            CandidateProfile,
            user=request.user,
            is_deleted=False
        )

        # Get uploaded file
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

        # Generate a unique filename
        import uuid
        uploaded_file.name = f"{uuid.uuid4().hex}{extension}"

        # Save resume
        profile.resume = uploaded_file
        profile.save()

        return Response(
            {
                "message": "Resume uploaded successfully.",
                "resume": profile.resume.name
            },
            status=status.HTTP_201_CREATED
        )
class ResumeDownloadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # Allow candidates and admins only
        if user.role not in ["CANDIDATE", "ADMIN"]:
            raise PermissionDenied(
                "Only candidates and admins can download resumes."
            )

        # Candidates can download only their own resume
        if user.role == "CANDIDATE":
            profile = get_object_or_404(
                CandidateProfile,
                user=user,
                is_deleted=False
            )

        # Admins must specify the candidate profile ID
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

        # Check whether a resume exists
        if not profile.resume:
            raise ValidationError(
                {"resume": "No resume uploaded."}
            )

        # Check whether the physical file exists
        if not profile.resume.storage.exists(profile.resume.name):
            raise ValidationError(
                {"resume": "Resume file not found in storage."}
            )

        # Return the file as a download
        return FileResponse(
            profile.resume.open("rb"),
            as_attachment=True,
            filename=os.path.basename(profile.resume.name)
        )
