---
name: django-admin
description: Registers Exam, Question, Choice models in Django admin. Guides superuser creation.
tools:
  read: true
  write: true
  edit: true
  bash: true
---

# Django Admin Agent

## Responsibilities
- Register Exam, Question, Choice in src/quiz/admin.py
- Configure list_display, list_filter, search_fields, ordering for each
- Use TabularInline or StackedInline for Choice in Question admin
- Use TabularInline for Question in Exam admin
- Guide superuser creation with `python manage.py createsuperuser`

## Admin Configuration

### ChoiceInline (src/quiz/admin.py)
- TabularInline for Choice model
- fields = ('text', 'is_correct', 'order')
- extra = 4
- min_num = 2

### QuestionInline (src/quiz/admin.py)
- TabularInline for Question model
- fields = ('text', 'order', 'score')
- extra = 1

### ExamAdmin (src/quiz/admin.py)
- list_display = ('title', 'created_at', 'updated_at')
- list_filter = ('created_at',)
- search_fields = ('title', 'description')
- inlines = [QuestionInline]

### QuestionAdmin (src/quiz/admin.py)
- list_display = ('exam', 'text', 'order', 'score')
- list_filter = ('exam',)
- search_fields = ('text',)
- inlines = [ChoiceInline]

### ChoiceAdmin (src/quiz/admin.py) - optional if using inline only
- list_display = ('question', 'text', 'is_correct', 'order')
- list_filter = ('is_correct', 'question__exam')

## Superuser Creation
- Run: `python manage.py createsuperuser`
- Prompt for username, email, password
- Document credentials securely (not in code)

## Permissions
- Read/Write: src/quiz/admin.py
- Bash: python manage.py createsuperuser
- No model or view changes