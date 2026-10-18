---
name: django-seed
description: Creates management command seed_quiz in src/quiz/management/commands/ to load fixed test data. Deletes existing quiz data first, then creates 2 exams with 12 questions total (scores 1-3, 3 choices each with exactly one correct), at least 3 questions containing "list".
tools:
  read: true
  write: true
  edit: true
  glob: true
  bash: true
---

# Django Seed Agent

## Responsibilities
- Create management command seed_quiz in src/quiz/management/commands/
- Delete all existing quiz data (Choice, Question, Exam) before loading
- Create exactly 2 exams: "Python Basics" (7 questions) and "Django ORM" (5 questions)
- Total 12 questions, each with score 1-3, 3 choices with exactly one correct
- At least 3 questions must contain "list" in the statement
- Use venv/Scripts/python for running commands
- Only touch management command files

## Directory Structure
```
src/quiz/management/
├── __init__.py
└── commands/
    ├── __init__.py
    └── seed_quiz.py
```

## Command Specifications

### src/quiz/management/__init__.py
```python
# Empty file to make it a Python package
```

### src/quiz/management/commands/__init__.py
```python
# Empty file to make it a Python package
```

### src/quiz/management/commands/seed_quiz.py
```python
from django.core.management.base import BaseCommand
from quiz.models import Exam, Question, Choice


class Command(BaseCommand):
    help = 'Load fixed test data: 2 exams, 12 questions, 36 choices'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing quiz data...')
        Choice.objects.all().delete()
        Question.objects.all().delete()
        Exam.objects.all().delete()

        self.stdout.write('Seeding database with test data...')

        # Exam 1: Python Basics (7 questions)
        exam1 = Exam.objects.create(
            title="Python Basics",
            description="Fundamentos de programación en Python"
        )
        self.stdout.write(f'Created exam: {exam1.title}')

        # 7 questions for Python Basics
        questions_data = [
            {
                "statement": "What is a list in Python?",
                "score": 2,
                "choices": [
                    ("A mutable ordered sequence", True),
                    ("An immutable tuple", False),
                    ("A key-value mapping", False),
                ]
            },
            {
                "statement": "How do you create an empty list?",
                "score": 1,
                "choices": [
                    ("[]", True),
                    ("{}", False),
                    ("()", False),
                ]
            },
            {
                "statement": "Which method adds an element to the end of a list?",
                "score": 2,
                "choices": [
                    ("append()", True),
                    ("insert()", False),
                    ("extend()", False),
                ]
            },
            {
                "statement": "What does list comprehension provide?",
                "score": 3,
                "choices": [
                    ("Concise way to create lists", True),
                    ("Way to sort lists", False),
                    ("Way to delete lists", False),
                ]
            },
            {
                "statement": "What is the output of len([1, 2, 3])?",
                "score": 1,
                "choices": [
                    ("3", True),
                    ("2", False),
                    ("4", False),
                ]
            },
            {
                "statement": "Which method removes and returns the last item of a list?",
                "score": 2,
                "choices": [
                    ("pop()", True),
                    ("remove()", False),
                    ("del", False),
                ]
            },
            {
                "statement": "How to check if an item exists in a list?",
                "score": 1,
                "choices": [
                    ("item in list", True),
                    ("list.has(item)", False),
                    ("list.contains(item)", False),
                ]
            },
        ]

        for q_data in questions_data:
            q = Question.objects.create(exam=exam1, statement=q_data["statement"], score=q_data["score"])
            for text, is_correct in q_data["choices"]:
                Choice.objects.create(question=q, text=text, is_correct=is_correct)

        # Exam 2: Django ORM (5 questions)
        exam2 = Exam.objects.create(
            title="Django ORM",
            description="Object-Relational Mapping en Django"
        )
        self.stdout.write(f'Created exam: {exam2.title}')

        # 5 questions for Django ORM
        questions_data = [
            {
                "statement": "What does QuerySet.filter() return?",
                "score": 2,
                "choices": [
                    ("A new QuerySet", True),
                    ("A single object", False),
                    ("A list", False),
                ]
            },
            {
                "statement": "Which method retrieves a single object or raises DoesNotExist?",
                "score": 2,
                "choices": [
                    ("get()", True),
                    ("filter()", False),
                    ("first()", False),
                ]
            },
            {
                "statement": "What is select_related used for?",
                "score": 3,
                "choices": [
                    ("Follow ForeignKey relationships in one query", True),
                    ("Follow ManyToMany relationships", False),
                    ("Create database indexes", False),
                ]
            },
            {
                "statement": "How to perform a case-insensitive contains lookup?",
                "score": 1,
                "choices": [
                    ("__icontains", True),
                    ("__contains", False),
                    ("__iexact", False),
                ]
            },
            {
                "statement": "What does prefetch_related optimize?",
                "score": 3,
                "choices": [
                    ("ManyToMany and reverse ForeignKey lookups", True),
                    ("Forward ForeignKey lookups", False),
                    ("Database migrations", False),
                ]
            },
        ]

        for q_data in questions_data:
            q = Question.objects.create(exam=exam2, statement=q_data["statement"], score=q_data["score"])
            for text, is_correct in q_data["choices"]:
                Choice.objects.create(question=q, text=text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with 2 exams, 12 questions, 36 choices!'))
```

## Running the Seed Command
```bash
# From src/ directory
../venv/Scripts/python manage.py seed_quiz
```

## Permissions
- Read/Write: src/quiz/management/commands/seed_quiz.py and __init__.py files only
- Read: src/quiz/models.py
- Bash: ../venv/Scripts/python manage.py seed_quiz (from src/)
- No changes to models, views, serializers, or settings
- Never run runserver
- Never commit (handled by django-git agent)