
from django.db import models
from django.conf import settings


class CandidateProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )

    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    expected_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Resume upload field
    resume = models.FileField(
        upload_to="resumes/",
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["is_deleted", "created_at"],
                name="cand_active_created_idx"
            ),
        ]

    def __str__(self):
        return f"Candidate Profile - {self.user.email}"
