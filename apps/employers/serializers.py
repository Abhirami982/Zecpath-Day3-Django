
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

    def validate_company_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Company name cannot be empty."
            )
        return value

    def validate_domain(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                "Domain cannot contain only spaces."
            )
        return value

    def validate_company_size(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                "Company size cannot contain only spaces."
            )
        return value
