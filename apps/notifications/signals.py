from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.issues.models import Issue, Comment, IssueFeedback
from .models import Notification

User = get_user_model()


def create_notification(user, issue, notification_type, message):
    """Helper function to create a notification"""
    Notification.objects.create(
        user=user, issue=issue, notification_type=notification_type, message=message
    )


@receiver(post_save, sender=Issue)
def issue_notification(sender, instance, created, **kwargs):
    """Create notifications when an issue is created or updated"""
    if created:
        # Notify all mentors in the cohort about the new issue
        mentors = User.objects.filter(role=User.MENTOR, cohort=instance.cohort)
        for mentor in mentors:
            create_notification(
                user=mentor,
                issue=instance,
                notification_type=Notification.ISSUE_CREATED,
                message=_(f"New issue reported: {instance.title}"),
            )

        # Also notify any admins
        admins = User.objects.filter(role=User.ADMIN)
        for admin in admins:
            create_notification(
                user=admin,
                issue=instance,
                notification_type=Notification.ISSUE_CREATED,
                message=_(f"New issue reported: {instance.title}"),
            )
    else:
        # Check if status has changed
        if hasattr(instance, "_status_changed") and instance._status_changed:
            # Notify the reporter
            if instance.reported_by:
                create_notification(
                    user=instance.reported_by,
                    issue=instance,
                    notification_type=Notification.ISSUE_UPDATED,
                    message=_(
                        f"Issue status changed to: {instance.get_status_display()}"
                    ),
                )

            # If resolved, notify mentors and admins
            if instance.status == Issue.RESOLVED:
                # Notify mentors in the cohort
                mentors = User.objects.filter(role=User.MENTOR, cohort=instance.cohort)
                for mentor in mentors:
                    create_notification(
                        user=mentor,
                        issue=instance,
                        notification_type=Notification.ISSUE_RESOLVED,
                        message=_(f"Issue resolved: {instance.title}"),
                    )

                # Notify admins
                admins = User.objects.filter(role=User.ADMIN)
                for admin in admins:
                    create_notification(
                        user=admin,
                        issue=instance,
                        notification_type=Notification.ISSUE_RESOLVED,
                        message=_(f"Issue resolved: {instance.title}"),
                    )


@receiver(pre_save, sender=Issue)
def track_issue_changes(sender, instance, **kwargs):
    """Track changes to issue status"""
    if instance.pk:
        try:
            old_instance = Issue.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                instance._status_changed = True

                # Track assignment changes
                if (
                    old_instance.assigned_to != instance.assigned_to
                    and instance.assigned_to
                ):
                    instance._newly_assigned = True
            else:
                instance._status_changed = False
        except Issue.DoesNotExist:
            pass


@receiver(post_save, sender=Issue)
def issue_assignment_notification(sender, instance, **kwargs):
    """Create notifications when an issue is assigned"""
    if hasattr(instance, "_newly_assigned") and instance._newly_assigned:
        # Notify the assignee
        create_notification(
            user=instance.assigned_to,
            issue=instance,
            notification_type=Notification.ISSUE_ASSIGNED,
            message=_(f"You have been assigned to: {instance.title}"),
        )


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    """Create notifications when a comment is added"""
    if created:
        # Notify the issue reporter
        if instance.issue.reported_by and instance.issue.reported_by != instance.user:
            create_notification(
                user=instance.issue.reported_by,
                issue=instance.issue,
                notification_type=Notification.COMMENT_ADDED,
                message=_(f"New comment on your issue: {instance.issue.title}"),
            )

        # Notify the assignee if different from commenter and reporter
        if (
            instance.issue.assigned_to
            and instance.issue.assigned_to != instance.user
            and instance.issue.assigned_to != instance.issue.reported_by
        ):
            create_notification(
                user=instance.issue.assigned_to,
                issue=instance.issue,
                notification_type=Notification.COMMENT_ADDED,
                message=_(f"New comment on issue: {instance.issue.title}"),
            )


@receiver(post_save, sender=IssueFeedback)
def feedback_notification(sender, instance, created, **kwargs):
    """Create notifications when feedback is added"""
    if created:
        # Notify the assignee
        if instance.issue.assigned_to:
            create_notification(
                user=instance.issue.assigned_to,
                issue=instance.issue,
                notification_type=Notification.FEEDBACK_ADDED,
                message=_(f"Feedback received on issue: {instance.issue.title}"),
            )

        # Notify mentors in the cohort
        mentors = User.objects.filter(role=User.MENTOR, cohort=instance.issue.cohort)
        for mentor in mentors:
            if mentor != instance.issue.assigned_to:  # Avoid duplicate for assignee
                create_notification(
                    user=mentor,
                    issue=instance.issue,
                    notification_type=Notification.FEEDBACK_ADDED,
                    message=_(f"Feedback received on issue: {instance.issue.title}"),
                )
