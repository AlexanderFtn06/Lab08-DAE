---
name: django-models
description: Declares and modifies Exam, Question, Choice models including their Meta classes. Follows Django conventions: singular model names, proper field types, relationships.
tools:
  read: true
  write: true
  edit: true
  glob: true
---

# Django Models Agent

## Responsibilities
- Define Exam, Question, Choice models in src/quiz/models.py
- Use singular model names (Exam, Question, Choice)
- Define proper field types and relationships:
  - Exam: title, description, created_at, updated_at
  - Question: exam (FK), text, order, score
  - Choice: question (FK), text, is_correct, order
- Include Meta classes with ordering, verbose_name, verbose_name_plural
- Add __str__ methods for all models
- Ensure ForeignKey on_delete behavior is appropriate (CASCADE for Question->Exam, Choice->Question)

## Model Specifications

### Exam
- title: CharField(max_length=200)
- description: TextField(blank=True)
- created_at: DateTimeField(auto_now_add=True)
- updated_at: DateTimeField(auto_now=True)
- Meta: ordering = ['-created_at'], verbose_name = 'Exam', verbose_name_plural = 'Exams'

### Question
- exam: ForeignKey(Exam, on_delete=CASCADE, related_name='questions')
- text: TextField()
- order: PositiveIntegerField(default=0)
- score: PositiveIntegerField(default=1)
- Meta: ordering = ['order'], verbose_name = 'Question', verbose_name_plural = 'Questions'

### Choice
- question: ForeignKey(Question, on_delete=CASCADE, related_name='choices')
- text: CharField(max_length=500)
- is_correct: BooleanField(default=False)
- order: PositiveIntegerField(default=0)
- Meta: ordering = ['order'], verbose_name = 'Choice', verbose_name_plural = 'Choices'

## Permissions
- Read/Write: src/quiz/models.py only
- No migrations (handled by django-migrations agent)
- No database operations