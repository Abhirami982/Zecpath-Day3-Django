
from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['employer']
        read_only_fields = [
            'id', 'created_at', 'updated_at'
        ]


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['status']


class PublicJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'skills',
            'experience',
            'salary_range',
            'location',
            'job_type',
            'created_at',
            'is_featured'
        ]
