---
name: django-templates
description: Creates ALL required templates: base, exam list, exam detail, AND question_form.html with full form and formset rendering real widgets ({{ form.field }}) and error block.
tools:
  - read
  - write
  - edit
  - glob
  - bash
---

# Django Templates Agent

## Responsibilities
- Create base.html with block structure
- Create quiz/exam_list.html extending base
- Create quiz/exam_detail.html extending base
- Create quiz/question_form.html with QuestionForm AND ChoiceFormSet complete
- Render REAL widgets for each field ({{ form.field }}, {{ formset }})
- Include error message block for validation errors
- Use proper Django template syntax

## Template Structure

### base.html (templates/base.html)
- Standard HTML5 structure
- Blocks: title, content, extra_css, extra_js
- Include bootstrap or basic CSS
- {% load static %}

### exam_list.html (templates/quiz/exam_list.html)
- Extends base.html
- Loop through exam_list
- Link to exam_detail using {% url 'quiz:exam_detail' exam.pk %}

### exam_detail.html (templates/quiz/exam_detail.html)
- Extends base.html
- Display exam title, description
- Loop through exam.questions.all with choices
- Link to question_create using {% url 'quiz:question_create' exam.pk %}

### question_form.html (templates/quiz/question_form.html) - CRITICAL
- Extends base.html
- Form tag with method="post" and {% csrf_token %}
- Render QuestionForm fields: {{ form.text }}, {{ form.order }}, {{ form.score }}
- Render ChoiceFormSet:
  - {{ formset.management_form }}
  - Loop through formset.forms:
    - {{ form.id }} (hidden)
    - {{ form.text }}, {{ form.is_correct }}, {{ form.order }}
- ERROR BLOCK: {% if formset.non_form_errors %}<div class="error">{{ formset.non_form_errors }}</div>{% endif %}
- Submit button

## Critical Rules
- MUST render actual widget: {{ form.field }} NOT just {{ form.field.label }}
- MUST create question_form.html BEFORE testing question_create view
- Include formset.management_form
- Show errors visibly in template, not just backend

## Permissions
- Read/Write: templates/ directory (base.html, quiz/*.html)
- Read: src/quiz/forms.py, src/quiz/views.py to understand form structure
- No Python code