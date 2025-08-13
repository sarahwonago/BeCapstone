from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.issues.models import Course, Project, Task

User = get_user_model()


class Command(BaseCommand):
    help = "Creates test data for development"

    def handle(self, *args, **options):
        # Create test course
        course, created = Course.objects.get_or_create(
            name="Backend Development", defaults={"duration_in_weeks": 12}
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Course {'created' if created else 'already exists'}: {course.name}"
            )
        )

        # Create test project
        project, created = Project.objects.get_or_create(
            name="Django Signals",
            course=course,
            week_number=4,
            defaults={"total_tasks": 5},
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Project {'created' if created else 'already exists'}: {project.name}"
            )
        )

        # Create test tasks
        for i in range(1, 6):
            task, created = Task.objects.get_or_create(
                project=project,
                task_number=i,
                defaults={"title": f"Task {i}: Implement signal {i}"},
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Task {'created' if created else 'already exists'}: {task.title}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Test data created successfully!"))
