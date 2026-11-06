
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import EmployerProfile
from .serializers import EmployerProfileSerializer


class EmployerProfileAPIView(generics.GenericAPIView):

    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role not in ["EMPLOYER", "ADMIN"]:
            raise PermissionDenied(
                "Only employers and admins can access employer profiles."
            )

        if user.role == "ADMIN":
            profile_id = self.request.query_params.get("id")

            if profile_id:
                return get_object_or_404(
                    EmployerProfile,
                    id=profile_id,
                    is_deleted=False
                )

        return get_object_or_404(
            EmployerProfile,
            user=user,
            is_deleted=False
        )

    def get(self, request):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "EMPLOYER":
            raise PermissionDenied(
                "Only employers can create employer profiles."
            )

        if EmployerProfile.objects.filter(user=request.user).exists():
            raise PermissionDenied(
                "Employer profile already exists."
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
            {"message": "Employer profile deleted successfully."}
        )

