from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Permission to only allow students to perform certain actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student()

    def __str__(self):
        return "Student access only"


class IsMentor(permissions.BasePermission):
    """
    Permission to only allow mentors to perform certain actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_mentor()

    def __str__(self):
        return "Mentor access only"


class IsAdmin(permissions.BasePermission):
    """
    Permission to only allow admins to perform certain actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

    def __str__(self):
        return "Admin access only"


class IsMentorOrAdmin(permissions.BasePermission):
    """
    Permission to only allow mentors or admins to perform certain actions.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_mentor() or request.user.is_admin()

    def __str__(self):
        return "Mentor or admin access only"


class IsOwnerOrMentorOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object, mentors, or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_mentor() or request.user.is_admin():
            return True

        # Assuming the object has a 'reported_by' field for user ownership
        if hasattr(obj, "reported_by"):
            return obj.reported_by == request.user

        # If the object is a user, check if it's the same user
        if hasattr(obj, "id"):
            return obj.id == request.user.id

        return False

    def __str__(self):
        return "Owner, mentor, or admin access only"
