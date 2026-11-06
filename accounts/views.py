from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm


def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("register_success")
    else:
        form = CustomUserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def register_success(request):
    return render(
        request,
        "accounts/register_success.html",
    )


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'role',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        return user


class SignupAPIView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

class ProtectedAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "You are successfully authenticated!",
            "username": request.user.username,
            "role": request.user.role
        })
