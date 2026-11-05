
from rest_framework import serializers
from .models import CandidateProfile


class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = [
            'id',
            'user',
            'skills',
            'education',
            'experience',
            'expected_salary',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at',
        ]

    def validate_skills(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Skills cannot be empty."
            )
        return value

    def validate_expected_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Expected salary cannot be negative."
            )
        return value

    def validate_education(self, value):
        if value and not value.strip():
            raise serializers.ValidationError(
                "Education cannot contain only spaces."
            )
        return value
