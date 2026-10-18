---
name: django-drf-setup
description: Installs and configures Django REST Framework and django-filter. Updates requirements.txt (UTF-8), INSTALLED_APPS, and REST_FRAMEWORK settings with pagination, permissions, and filters.
tools:
  read: true
  write: true
  edit: true
  bash: true
---

# Django DRF Setup Agent

## Responsibilities
- Install djangorestframework and django-filter using venv/Scripts/python
- Update requirements.txt (convert to UTF-8 encoding)
- Add 'rest_framework', 'django_filters' to INSTALLED_APPS in settings.py
- Configure REST_FRAMEWORK dictionary in settings.py with:
  - DEFAULT_PAGINATION_CLASS: PageNumberPagination
  - PAGE_SIZE: 20
  - DEFAULT_PERMISSION_CLASSES: [IsAuthenticatedOrReadOnly]
  - DEFAULT_FILTER_BACKENDS: [DjangoFilterBackend, SearchFilter, OrderingFilter]
- Only touch requirements.txt and settings.py
- Use venv/Scripts/python for all commands

## Installation Steps

### 1. Install packages
```bash
venv/Scripts/python -m pip install djangorestframework django-filter
```

### 2. Update requirements.txt (UTF-8)
- Read current requirements.txt (may be UTF-16)
- Write back as UTF-8 with added packages:
  - djangorestframework
  - django-filter

### 3. Update settings.py (src/config/config/settings.py)
```python
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'django_filters',
    'quiz',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Permissions
- Read/Write: requirements.txt, src/config/config/settings.py only
- Bash: venv/Scripts/python -m pip install ...
- No model, view, serializer, or URL changes
- Never run runserver
- Never commit (handled by django-git agent)