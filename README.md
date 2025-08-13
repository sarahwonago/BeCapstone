# ALX Curriculum Issue Reporting System

A dedicated web-based tool for structured issue submission, mentor responses, and admin oversight, especially related to cohort-specific content and curriculum integrity.

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m virtualenv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env.example`
6. Run migrations: `python manage.py migrate`
7. Create admin user: `python manage.py create_admin`
8. Run the server: `python manage.py runserver`

## Gitflow Workflow

This project uses Gitflow workflow:

- `main` branch contains production code
- `develop` branch contains development code
- Feature branches are created from `develop` and merged back when complete
- Release branches are created from `develop` when ready for release
- Hotfix branches are created from `main` for emergency fixes

### Creating a new feature

```bash
git flow feature start feature-name
# Work on your feature...
git flow feature finish feature-name
```

# User Authentication Flow

The ALX Curriculum Issue Reporting System uses JWT (JSON Web Token) authentication with role-based access control.

## Authentication Endpoints

| Endpoint                      | Method | Description                     |
| ----------------------------- | ------ | ------------------------------- |
| `/api/auth/register/`         | POST   | Register a new user account     |
| `/api/auth/login/`            | POST   | Login and obtain JWT tokens     |
| `/api/auth/refresh/`          | POST   | Refresh an expired access token |
| `/api/users/me/`              | GET    | Get current user details        |
| `/api/users/change_password/` | POST   | Change user password            |

## Registration Process

Users can register with the following information:

- Username
- Email
- Password (with confirmation)
- First and last name
- Role (student, mentor, or admin)
- Cohort (for students and mentors)

Example registration request:

```json
{
  "username": "student1",
  "email": "student1@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "cohort": "Cohort1_BE"
}
```

### Role-Based Access

The system has three user roles with different permissions:

- Student: Can create and view their own issues
- Mentor: Can view and respond to issues from students in their cohort
- Admin: Has full access to all system features and user management

## For Future Implementation

1. **Admin-Controlled Registration**:

   - Make all new registrations default to "student" role
   - Create an admin endpoint to change user roles
   - Only admins can promote users to mentor/admin roles

2. **Invitation System**:

   - Generate unique invitation codes for mentor/admin registrations
   - Only users with valid codes can register as non-students
   - Track which admin created each invitation code

3. **Email Domain Verification**:
   - Restrict mentor/admin roles to specific email domains
   - For example, only `@alx.org` emails can register as mentors/admins
