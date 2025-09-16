# Django Job Portal (Interview-ready Project)

A simple but complete recruitment system built with Django.

## Features
- Role-based auth: Candidate & Employer
- Candidates: profile, resume upload, apply to jobs
- Employers: post jobs, view applicants & resumes
- Job list with search & filters
- Clean Bootstrap UI
- Django Admin

## Quickstart

```bash
# 1) Create venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install deps
pip install "Django>=4.2,<6"

# 3) Setup project
python manage.py migrate
python manage.py createsuperuser  # optional, for admin

# 4) Run
python manage.py runserver
```

Open: http://127.0.0.1:8000

## Usage
- Sign up and choose **Candidate** or **Employer**.
- Employer → Post jobs and view applicants.
- Candidate → Update profile & resume, apply to jobs.

## Notes
- Uploaded resumes are stored in `media/resumes/`.
- Default DB is SQLite. For production, configure PostgreSQL in `settings.py`.
