from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access control."""

    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (STUDENT, "Student"),
        (MENTOR, "Mentor"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    cohort = models.CharField(max_length=50, blank=True, null=True)

    def is_student(self):
        return self.role == self.STUDENT

    def is_mentor(self):
        return self.role == self.MENTOR

    def is_admin(self):
        return self.role == self.ADMIN
