
from django.db import models
from apps.employers.models import EmployerProfile


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DRAFT', 'Draft'),
    ]

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField()
    experience = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
            models.Index(fields=['location']),
            models.Index(fields=['job_type']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return self.title
