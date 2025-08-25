# ALX Curriculum Issue Reporting System

**Capstone Project Proposal**

---

## 1. Project Idea

**Title:** ALX Curriculum Issue Reporting System

**Summary:**  
The current method for handling learner issues in ALX relies heavily on Discord, which lacks structure, accountability, and visibility. Students often tag mentors in chat threads, but mentors may miss messages or struggle to manage high volumes. Furthermore, there is no central place to track problems with curriculum content (e.g., broken checkers, unclear instructions, typos).

This project proposes a **dedicated web-based tool** for structured issue submission, mentor responses, and admin oversight, especially related to cohort-specific content and curriculum integrity.

This project will:

- Help students raise issues clearly and track responses.
- Help mentors manage and respond to curriculum-related issues efficiently.
- Help admins and curriculum teams monitor issue trends and mentor responsiveness.

---

## 2. Project Features

### For Students:

- Submit issues by category (e.g., checker error, unclear instructions, typos).
- Select specific cohort, course, week, project, and task affected.
- Track issue status: `Open`, `In Progress`, `Resolved`.
- View mentor responses and comments.
- Rate satisfaction with the resolution.
- View personal reporting history.
- **Upload file attachments** (screenshots, logs, error messages).
- **Access issue templates** for common problem types.
- **Search existing issues** to see if their problem has been reported.
- **Offline capability** to draft issues when connectivity is poor.

### For Mentors:

- View and filter issues by cohort, course, week, project, task, urgency.
- Comment and update issue status.
- Track personal performance (response times, resolution rates).
- **Perform batch operations** on multiple similar issues simultaneously.
- **Convert resolved issues** to knowledge base articles.
- **Create templates** for common responses.

### For Admins/Curriculum Team:

- View all issues across all cohorts and courses.
- Filter issues by project/task, frequency, resolution delay.
- Assign or escalate issues.
- Generate reports:
  - Average response/resolution time
  - Satisfaction scores
  - Frequent problem areas
- **Advanced analytics dashboard** with visualizations of issue trends.
- **Knowledge base management** for converting resolved issues to documentation.

### Additional Features:

- SLA tracking (time to first response, time to resolution).
- Feedback collection (1–5 rating + comments).
- Issue history log (actions + timestamps).
- Admin analytics dashboard (charts, cohort trends, most common issue types).
- **Notification system** (email, in-app, optional SMS) for issue updates.
- **Robust search functionality** across all issues and knowledge base.
- **Mobile-responsive design** for all user interfaces.

---

## 3. Technical Stack & Architecture

### Frontend:

- **React.js** for component-based UI development
- **Bootstrap or Material UI** for responsive design
- **Redux** for state management
- **PWA capabilities** for offline support

### Backend:

- Django with Django REST Framework
- PostgreSQL for relational data storage
- Redis for caching and real-time notifications

### Authentication:

- JWT-based authentication
- Role-based access control (RBAC)
- Integration with existing ALX authentication system (if available)

### Deployment:

- Docker containers for consistent deployment
- CI/CD pipeline with GitHub Actions
- Hosted on AWS (EC2 or ECS for application, RDS for database)
- Nginx as reverse proxy with SSL

---

## 4. APIs

For the MVP, **no external APIs** are required.

**Potential future integrations:**

- Integration with ALX Learning Management System
- Integration with Discord for critical notifications
- GitHub integration for code-related issues

---

## 5. Models & API Endpoints

### Models:

- **User:** `name`, `email`, `role` (student/mentor/admin), `cohort`
- **Course:** `name`, `duration_in_weeks`
- **Project:** `name`, `course` (FK), `week_number`, `total_tasks`
- **Task:** `project` (FK), `task_number`, `title`
- **Issue:**
  - `title`, `description`, `category` (typo/checker/etc), `urgency`, `status` (open/in progress/resolved)
  - `reported_by` (FK → User)
  - `assigned_to` (nullable FK → User)
  - `course` (FK), `cohort`, `week_number`
  - `project` (FK), `task` (nullable FK)
  - `created_at`, `first_response_at`, `resolved_at`
- **Comment:** `issue` (FK), `user` (FK), `content`, `created_at`
- **IssueFeedback:** `issue` (OneToOne FK), `rating` (1–5), `comment`
- **IssueHistory:** `issue` (FK), `action`, `performed_by` (FK), `timestamp`
- **Attachment:** `issue` (FK), `file`, `uploaded_by` (FK), `uploaded_at`
- **IssueTemplate:** `title`, `description_template`, `category`, `created_by` (FK)
- **KnowledgeBaseArticle:** `title`, `content`, `related_issue` (FK), `tags`, `created_at`, `updated_at`
- **Notification:** `user` (FK), `issue` (FK), `message`, `type`, `is_read`, `created_at`

### API Endpoints (Django REST Framework):

| Endpoint                        | Method | Description                    |
| ------------------------------- | ------ | ------------------------------ |
| `/api/issues/`                  | GET    | List all issues (mentor/admin) |
| `/api/issues/`                  | POST   | Create new issue (student)     |
| `/api/issues/<id>/`             | GET    | View issue detail              |
| `/api/issues/<id>/`             | PATCH  | Update status / assignment     |
| `/api/issues/comments/`         | POST   | Add comment                    |
| `/api/issues/feedback/`         | POST   | Add feedback after resolution  |
| `/api/issues/search/`           | GET    | Search across issues           |
| `/api/issues/<id>/attachments/` | POST   | Upload attachment              |
| `/api/templates/`               | GET    | List issue templates           |
| `/api/kb/`                      | GET    | Access knowledge base articles |
| `/api/issues/batch/`            | PATCH  | Update multiple issues         |
| `/api/notifications/`           | GET    | Get user notifications         |
| `/api/notifications/<id>/read/` | POST   | Mark notification as read      |

---

## 6. System Flow Overview

**Scenario:**  
A student in **Cohort1_BE** is working on the **Django Signals Project (Week 4)**. Task 2 has a broken checker.

**Step-by-Step Flow:**

**Student:**

1. Logs in and navigates to "Report Issue" form.
2. Selects:
   - Cohort: `Cohort1_BE`
   - Course: `Backend Development`
   - Week: `4`
   - Project: `Django Signals`
   - Task: `Task 2`
3. Selects category: `Checker not working`
4. Describes the issue, attaches screenshot, and submits.

**System:**

- Saves issue with status = `Open`.
- Notifies mentors for that cohort/course via in-app and email notifications.
- Starts SLA timer.

**Mentor:**

- Views open issues.
- Filters, comments, changes status to `In Progress`.
- Resolves or escalates.

**Student:**

- Gets resolution notification.
- Gives feedback rating.

**Admin:**

- Monitors trends, SLA compliance, and problem areas.
- Converts common issues to knowledge base articles.

---

## 7. Project Plan (5 Weeks)

### **Week 1 – Idea & Planning**

- Finalize idea and MVP features.
- Draft ERD and model relations.
- Define tech stack (Django, DRF, PostgreSQL, React frontend).
- Deliverables: Final proposal, model sketches.

### **Week 2 – Design Phase**

- Create ERD & database schema.
- Map API endpoints.
- Wireframes for UI (desktop and mobile).
- Authentication system design.
- Deliverables: ERD, endpoint plan, wireframes.

### **Week 3 – Start Building**

- Implement models & serializers.
- Student submission flow.
- Role-based authentication.
- File upload functionality.
- Deliverables: Core issue reporting API.

### **Week 4 – Continue Building**

- Mentor/admin flows.
- SLA tracking.
- Cohort/course filters.
- Notification system.
- Frontend implementation.
- Deliverables: Full backend logic + dashboards.

### **Week 5 – Finalize & Submit**

- End-to-end testing.
- Deploy app with CI/CD pipeline.
- Mobile responsiveness testing.
- Knowledge base implementation.
- Deliverables: Live app, GitHub repo, demo video.

---

## 8. Detailed System Workflow

**Example Walkthrough:**

1. **Student** reports a checker error (high urgency) and attaches screenshot.
2. **System** logs issue, starts SLA timers, and notifies mentor.
3. **Mentor** assigns issue, comments, sets `in_progress`.
4. **Admin** notices trend, escalates if needed.
5. **Mentor** resolves issue, updates status to `resolved`.
6. **Student** gets notification, gives feedback (rating + comment).
7. **Admin** reviews analytics for trends and SLA performance.
8. **Mentor** converts the solution to a knowledge base article for future reference.

---

## 9. Summary of System Roles

| Role    | Actions                                                           |
| ------- | ----------------------------------------------------------------- |
| Student | Report issues, track status, give feedback, search knowledge base |
| Mentor  | Filter, assign, comment, resolve, meet SLA, create KB articles    |
| Admin   | View trends, escalate, send announcements, manage knowledge base  |

---

## 10. Scalability & Future Expansion

### Scalability Considerations:

- Database indexing for efficient querying as issue volume grows
- Caching layer for frequently accessed data
- Pagination for large result sets
- Horizontal scaling capability through containerization

### Future Expansion:

- Integration with ALX curriculum management system
- Mobile app version
- AI-powered issue categorization and routing
- Automated issue resolution for common problems
- Internationalization for multiple languages
- Advanced analytics with machine learning to

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
