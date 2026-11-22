# CareerConnect — Member 1: Job Seeker Module

A standalone, responsive Django job seeker implementation. The homepage features a custom animated SVG job-seeker illustration, responsive job search, live database counters, featured listings, career categories, and scroll-reveal effects. Includes registration, login/logout, editable profile, resume upload (PDF/DOC/DOCX, 5 MB max), job search and filters, job details, job applications, status tracking, dashboard, and Django admin for jobs/statuses.

## Windows quick start (PowerShell or VS Code terminal)

```powershell
cd CareerConnect_Member1_JobSeeker
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_jobs
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and admin at http://127.0.0.1:8000/admin/.

**If PowerShell blocks activation**, use `.venv\Scripts\python.exe` instead of `python` in each command, and `.venv\Scripts\pip.exe install -r requirements.txt`.

## Test the entire workflow
1. Register a job seeker and log in.
2. Open My Profile, add information, and upload a PDF/DOC/DOCX resume under 5 MB.
3. Search jobs by keyword, location, and job type; open a job.
4. Click Apply, write an optional cover letter, and submit.
5. Open My Applications to see the status. Admin can change the status in Django admin.

## Database
Default SQLite creates `db.sqlite3` automatically on `migrate`; no MySQL Workbench is needed for local testing. If your team uses MySQL, coordinate the **shared** `config/settings.py` DATABASES setting and credentials before merging. Do not commit DB passwords or the SQLite database.

## Team integration
This ZIP is a **standalone Django project for Member 1**, not a patch to your teammates' project. In a shared repository, copy `job_seeker/`, `templates/job_seeker/`, and `static/css/style.css`, add `job_seeker` to INSTALLED_APPS, include `job_seeker.urls` in root URLs, and configure MEDIA_URL/MEDIA_ROOT and template/static directories. **Important:** If Member 2 already has a `Job` or `JobApplication` model, DO NOT keep duplicate models. Agree on one canonical model and adjust imports/foreign keys before running migrations. Merge with the team's existing settings and URLs rather than overwriting them.

## GitHub branch (from your team's repository root)
```bash
git checkout main
git pull origin main
git checkout -b feature/job-seeker
git add .
git commit -m "Build complete job seeker module with resume upload and job search"
git push -u origin feature/job-seeker
```
Create a PR targeting `main` as requested in Issue #1. If your branch already exists, switch to it instead of creating a new branch. Never commit `.venv`, `media`, database, or secrets.

## Production notes
This is a working **development/demo implementation**, not a production security audit. Before public deployment, set a strong secret key, DEBUG=0, ALLOWED_HOSTS, HTTPS, production media storage and access controls, malware scanning of uploaded resumes, stricter content validation and file serving permissions, and deployment-grade database/static settings. Uploaded resumes are served by Django only in DEBUG mode; production must protect resume privacy. Only staff should access admin.
