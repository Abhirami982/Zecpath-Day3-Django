from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from core.models import Candidate, Employer


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.role == 'CANDIDATE':
        Candidate.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': instance.get_full_name() or instance.email
            }
        )

    elif instance.role == 'EMPLOYER':
        Employer.objects.get_or_create(
            user=instance,
            defaults={
                'company_name': instance.get_full_name() or instance.email
            }
        )


@receiver(post_save, sender=CustomUser)
def sync_user_profile(sender, instance, created, **kwargs):

    if created:
        return

    if instance.role == 'CANDIDATE':
        Candidate.objects.filter(user=instance).update(
            full_name=instance.get_full_name() or instance.email
        )

    elif instance.role == 'EMPLOYER':
        Employer.objects.filter(user=instance).update(
            company_name=instance.get_full_name() or instance.email
        )
