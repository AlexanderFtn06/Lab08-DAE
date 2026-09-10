---
name: django-views
description: Creates list, detail, and question create views with "exactly one correct choice" validation. On validation failure: no save, re-render form with user data, show visible error message.
tools:
  read: true
  write: true
  edit: true
  glob: true
---

# Django Views Agent

## Responsibilities
- Create ExamListView (list of exams)
- Create ExamDetailView (exam detail with questions)
- Create QuestionCreateView (create question with choices formset)
- Implement "exactly one correct choice" business rule validation
- On validation failure: (a) don't save, (b) re-render form with user's data, (c) show visible error message

## View Specifications

### ExamListView (src/quiz/views.py)
- ListView for Exam model
- Template: quiz/exam_list.html
- Context: exam_list or object_list
- Pagination optional

### ExamDetailView (src/quiz/views.py)
- DetailView for Exam model
- Template: quiz/exam_detail.html
- Context: exam (or object)
- Include questions with choices

### QuestionCreateView (src/quiz/views.py)
- CreateView or function-based view for Question with ChoiceFormSet
- Template: quiz/question_form.html (MUST exist before testing)
- Handle GET: render empty forms
- Handle POST:
  1. Validate QuestionForm and ChoiceFormSet
  2. Check "exactly one correct choice" rule
  3. If valid: save Question, then save ChoiceFormSet with question FK
  4. If invalid: re-render with submitted data + error message
- Redirect to exam_detail on success (use 'quiz:exam_detail' namespace)

## Validation Logic (Critical)
```python
# In POST handler after form.is_valid() and formset.is_valid():
correct_count = sum(1 for form in formset.cleaned_data if form.get('is_correct'))
if correct_count != 1:
    # Add error to formset non_form_errors or form
    formset.non_form_errors().append("Debe haber exactamente una opción correcta.")
    # Re-render with submitted data - DO NOT SAVE
    return render(request, template, {'form': form, 'formset': formset})
```

## URL Namespace Rule
- If quiz/urls.py has app_name = 'quiz', ALL redirects and {% url %} must use 'quiz:' prefix
- Example: redirect('quiz:exam_detail', pk=exam.pk)

## Permissions
- Read/Write: src/quiz/views.py only
- Read: src/quiz/forms.py, src/quiz/models.py
- No template creation (handled by django-templates agent)