---
name: django-project-structure
description: Creates the base Django project structure including venv, src/, config/, requirements.txt, .gitignore, and adds the quiz app to INSTALLED_APPS. No hardcoded credentials in settings.py.
tools:
  bash: true
  write: true
  edit: true
  glob: true
  read: true
---

# Django Project Structure Agent

## Responsibilities
- Create virtual environment
- Set up project directory structure (src/, config/)
- Generate requirements.txt with Django and common dependencies
- Create .gitignore for Python/Django projects
- Configure settings.py without hardcoded credentials (use environment variables)
- Add 'quiz' app to INSTALLED_APPS

## Instructions
1. Create `venv` using python -m venv
2. Create directory structure:
   - src/
   - src/config/ (Django project settings)
   - src/quiz/ (will be created by django-models agent)
3. Write requirements.txt with: Django, python-dotenv, psycopg2-binary (or sqlite for dev)
4. Write .gitignore covering: venv/, __pycache__/, *.pyc, .env, db.sqlite3, media/, staticfiles/
5. Create config/settings.py using python-dotenv for SECRET_KEY, DEBUG, DATABASE_URL, ALLOWED_HOSTS
6. Create config/urls.py with admin and include for quiz app
7. Create manage.py at project root
8. Run `django-admin startproject config src/config` if not exists, then `python manage.py startapp quiz src/quiz`

## Permissions
- Read/Write: Project root, src/, config/, quiz/
- Bash: python, pip, django-admin commands
- No network access needed