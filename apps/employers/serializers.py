
from rest_framework import serializers
from .models import EmployerProfile


class EmployerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployerProfile
        fields = [
            'id',
            'user',
            'company_name',
            'domain',
            'company_size',
            'is_verified',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'user',
            'is_verified',
            'created_at',
            'updated_at',
        ]
