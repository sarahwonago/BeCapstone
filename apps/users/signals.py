from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    """
    Log when a new user is created.
    """
    if created:
        logger.info(
            f"New user created: {instance.username} (Role: {instance.role}, Cohort: {instance.cohort})"
        )
