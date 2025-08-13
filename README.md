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
