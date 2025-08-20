import os
import uuid
import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def validate_file_size(file):
    """
    Validate that the file is under the maximum allowed size.
    """
    if file.size > settings.MAX_UPLOAD_SIZE:
        max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise ValidationError(
            f"File size exceeds the maximum allowed size ({max_size_mb:.1f}MB)."
        )


def validate_file_type(file):
    """
    Validate that the file is of an allowed type using python-magic.
    """
    # Read the first 2048 bytes to determine file type
    file_header = file.read(2048)
    file.seek(0)  # Reset file pointer

    # Use python-magic to detect MIME type
    mime = magic.from_buffer(file_header, mime=True)

    if mime not in settings.ALLOWED_MIME_TYPES:
        raise ValidationError(
            f"File type '{mime}' is not allowed. Please upload a file with one of the following types: "
            f"{', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
        )

    # Double-check extension as well
    ext = os.path.splitext(file.name)[1][1:].lower()
    if ext not in settings.ALLOWED_FILE_EXTENSIONS:
        raise ValidationError(
            f"File extension '{ext}' is not allowed. Please upload a file with one of the following extensions: "
            f"{', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
        )


def sanitize_filename(filename):
    """
    Sanitize a filename to prevent path traversal and ensure uniqueness.
    """
    # Get name and extension
    name, ext = os.path.splitext(filename)

    # Slugify the name to remove special characters
    name = slugify(name)

    # Truncate name if too long (max 100 chars)
    if len(name) > 100:
        name = name[:100]

    # Add a UUID to ensure uniqueness
    unique_name = f"{name}_{uuid.uuid4().hex[:8]}{ext}"

    return unique_name


def get_safe_file_path(instance, filename):
    """
    Generate a safe path for file uploads, organizing by issue ID.
    """
    # Sanitize the filename
    clean_filename = sanitize_filename(filename)

    # Get the issue ID or use 'temp' if not available
    issue_id = getattr(instance, "issue_id", "temp")

    # Return the path
    return f"attachments/issues/{issue_id}/{clean_filename}"
