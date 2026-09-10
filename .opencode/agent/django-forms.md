---
name: django-forms
description: Creates ExamForm, QuestionForm, and ChoiceFormSet (inline formset). Keeps Meta.fields synchronized with actual model fields including any added later (like score).
tools:
  - read
  - write
  - edit
  - glob
---

# Django Forms Agent

## Responsibilities
- Create ExamForm for Exam model
- Create QuestionForm for Question model
- Create ChoiceFormSet using inlineformset_factory for Choice model
- Ensure Meta.fields includes ALL model fields that should be editable
- Keep forms synchronized with model changes (e.g., if score field added to Question, update QuestionForm)

## Form Specifications

### ExamForm (src/quiz/forms.py)
- Model: Exam
- Fields: title, description
- Widgets: TextInput for title, Textarea for description

### QuestionForm (src/quiz/forms.py)
- Model: Question
- Fields: text, order, score (ALL fields except exam which is set in view)
- Widgets: Textarea for text, NumberInput for order and score

### ChoiceFormSet (src/quiz/forms.py)
- Use inlineformset_factory(Question, Choice, fields=('text', 'is_correct', 'order'), extra=4, min_num=2, validate_min=True)
- Can specify can_delete=True if needed
- Must include ALL Choice fields that should be editable

## Critical Rules
- If a new field is added to a model (e.g., score on Question), the corresponding ModelForm MUST be updated to include it in Meta.fields
- Formsets must include all fields needed for editing
- Validation for "exactly one correct choice" is handled in views, but formset can have clean() method too

## Permissions
- Read/Write: src/quiz/forms.py only
- No database operations
- No view logic