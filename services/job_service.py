
from core.models import Job


def get_all_jobs():
    """Return all jobs stored in the database."""
    return Job.objects.all()
