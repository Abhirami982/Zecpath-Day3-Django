
from rest_framework import serializers
from .models import Application


class CandidatePipelineSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source="candidate.full_name",
        read_only=True
    )
    candidate_email = serializers.EmailField(
        source="candidate.user.email",
        read_only=True
    )
    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "candidate",
            "candidate_name",
            "candidate_email",
            "job",
            "job_title",
            "status",
            "applied_at",
            "updated_at",
        ]
        read_only_fields = fields
