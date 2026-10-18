---
name: django-api-views
description: Creates ModelViewSet in src/quiz/api_views.py, DefaultRouter in src/quiz/api_urls.py, and includes api/ route in src/config/config/urls.py. Optimized querysets with select_related/prefetch_related/annotate. filterset_fields and search_fields configured.
tools:
  read: true
  write: true
  edit: true
  glob: true
---

# Django API Views Agent

## Responsibilities
- Create src/quiz/api_views.py with ModelViewSet classes for Exam, Question, Choice
- Create src/quiz/api_urls.py with DefaultRouter
- Include 'api/' route in src/config/config/urls.py
- Optimize querysets with select_related, prefetch_related, annotate
- Configure filterset_fields, search_fields, ordering_fields
- Do NOT touch src/quiz/views.py or src/quiz/urls.py from Lab 03
- Only touch api_views.py, api_urls.py, and config/urls.py

## API Views Specifications

### src/quiz/api_views.py
```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Prefetch
from .models import Exam, Question, Choice
from .serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return Exam.objects.annotate(
            questions_count=Count('questions', distinct=True)
        ).prefetch_related(
            Prefetch('questions', queryset=Question.objects.annotate(
                choices_count=Count('choices')
            ).prefetch_related('choices'))
        )


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam', 'score']
    search_fields = ['statement']
    ordering_fields = ['id', 'score']
    ordering = ['id']

    def get_queryset(self):
        return Question.objects.select_related('exam').prefetch_related('choices').annotate(
            choices_count=Count('choices')
        )


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['question', 'is_correct']
    search_fields = ['text']
    ordering_fields = ['id']
    ordering = ['id']

    def get_queryset(self):
        return Choice.objects.select_related('question__exam')
```

### src/quiz/api_urls.py
```python
from rest_framework.routers import DefaultRouter
from .api_views import ExamViewSet, QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')

urlpatterns = router.urls
```

### src/config/config/urls.py (add to existing urlpatterns)
```python
from django.urls import path, include

urlpatterns = [
    # ... existing patterns
    path('api/', include('quiz.api_urls')),
]
```

## Permissions
- Read/Write: src/quiz/api_views.py, src/quiz/api_urls.py, src/config/config/urls.py
- Read: src/quiz/models.py, src/quiz/serializers.py
- No changes to src/quiz/views.py or src/quiz/urls.py
- Never run runserver
- Never commit (handled by django-git agent)