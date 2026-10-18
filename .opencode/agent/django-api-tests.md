---
name: django-api-tests
description: Writes APITestCase tests in src/quiz/tests.py covering CRUD with status codes, 400/404 errors, filters, search, and pagination. Runs tests with ../venv/Scripts/python manage.py test quiz from src/.
tools:
  read: true
  write: true
  edit: true
  glob: true
  bash: true
---

# Django API Tests Agent

## Responsibilities
- Write APITestCase tests in src/quiz/tests.py
- Test CRUD operations with correct status codes (200, 201, 204, 400, 404)
- Test validation errors (exactly one correct choice, minimum two choices)
- Test filterset_fields, search_fields, ordering
- Test pagination (page size, page navigation)
- Run tests from src/ using ../venv/Scripts/python manage.py test quiz
- Only touch src/quiz/tests.py

## Test Specifications

### Test Structure
```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from quiz.models import Exam, Question, Choice


class ExamAPITestCase(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Test Exam", description="Description")
        self.question = Question.objects.create(exam=self.exam, statement="Q1", score=5)
        self.choice1 = Choice.objects.create(question=self.question, text="Correct", is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question, text="Wrong", is_correct=False)

    # LIST - GET /api/exams/
    def test_list_exams(self):
        url = reverse('exam-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    # CREATE - POST /api/exams/
    def test_create_exam_success(self):
        url = reverse('exam-list')
        data = {"title": "New Exam", "description": "Desc"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Exam")

    def test_create_exam_invalid(self):
        url = reverse('exam-list')
        data = {"description": "Missing title"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # RETRIEVE - GET /api/exams/{id}/
    def test_retrieve_exam(self):
        url = reverse('exam-detail', kwargs={'pk': self.exam.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.exam.title)

    def test_retrieve_exam_404(self):
        url = reverse('exam-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # UPDATE - PUT/PATCH /api/exams/{id}/
    def test_update_exam(self):
        url = reverse('exam-detail', kwargs={'pk': self.exam.pk})
        data = {"title": "Updated", "description": "New desc"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated")

    # DELETE - DELETE /api/exams/{id}/
    def test_delete_exam(self):
        url = reverse('exam-detail', kwargs={'pk': self.exam.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exam.objects.filter(pk=self.exam.pk).exists())

    # FILTERS
    def test_filter_exams_by_title(self):
        url = reverse('exam-list')
        response = self.client.get(url, {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # SEARCH
    def test_search_exams(self):
        url = reverse('exam-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # PAGINATION
    def test_pagination(self):
        # Create 25 exams to test pagination (page_size=20)
        for i in range(25):
            Exam.objects.create(title=f"Exam {i}", description=f"Desc {i}")
        url = reverse('exam-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)
        self.assertIsNotNone(response.data['next'])
        # Test page 2
        response2 = self.client.get(response.data['next'])
        self.assertEqual(len(response2.data['results']), 6)


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Test Exam", description="Desc")
        self.question = Question.objects.create(exam=self.exam, statement="Q1", score=5)
        self.choice1 = Choice.objects.create(question=self.question, text="Correct", is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question, text="Wrong", is_correct=False)

    # CREATE with nested choices - VALID
    def test_create_question_with_choices_valid(self):
        url = reverse('question-list')
        data = {
            "exam": self.exam.id,
            "statement": "New Question",
            "score": 3,
            "choices": [
                {"text": "Choice A", "is_correct": True},
                {"text": "Choice B", "is_correct": False},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['statement'], "New Question")
        self.assertEqual(len(response.data['choices']), 2)

    # CREATE - exactly one correct choice validation
    def test_create_question_zero_correct_choices(self):
        url = reverse('question-list')
        data = {
            "exam": self.exam.id,
            "statement": "Q?",
            "choices": [
                {"text": "A", "is_correct": False},
                {"text": "B", "is_correct": False},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('choices', response.data)

    def test_create_question_two_correct_choices(self):
        url = reverse('question-list')
        data = {
            "exam": self.exam.id,
            "statement": "Q?",
            "choices": [
                {"text": "A", "is_correct": True},
                {"text": "B", "is_correct": True},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # CREATE - minimum two choices validation
    def test_create_question_one_choice(self):
        url = reverse('question-list')
        data = {
            "exam": self.exam.id,
            "statement": "Q?",
            "choices": [
                {"text": "A", "is_correct": True},
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # FILTER by exam
    def test_filter_questions_by_exam(self):
        url = reverse('question-list')
        response = self.client.get(url, {'exam': self.exam.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # SEARCH
    def test_search_questions(self):
        url = reverse('question-list')
        response = self.client.get(url, {'search': 'Q1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ChoiceAPITestCase(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Test Exam", description="Desc")
        self.question = Question.objects.create(exam=self.exam, statement="Q1", score=5)
        self.choice = Choice.objects.create(question=self.question, text="Correct", is_correct=True)

    def test_list_choices(self):
        url = reverse('choice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_choices_by_question(self):
        url = reverse('choice-list')
        response = self.client.get(url, {'question': self.question.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_choices_by_is_correct(self):
        url = reverse('choice-list')
        response = self.client.get(url, {'is_correct': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
```

## Running Tests
```bash
# From src/ directory
../venv/Scripts/python manage.py test quiz
```

## Permissions
- Read/Write: src/quiz/tests.py only
- Read: src/quiz/models.py, src/quiz/serializers.py, src/quiz/api_views.py
- Bash: ../venv/Scripts/python manage.py test quiz (from src/)
- No changes to views, urls, serializers, or models
- Never run runserver
- Never commit (handled by django-git agent)