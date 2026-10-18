"""API ViewSets for the quiz app."""
from rest_framework import viewsets
from quiz.models import Exam, Question, Choice
from quiz.serializers import ExamSerializer, QuestionSerializer, ChoiceSerializer


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet for Exam model."""
    queryset = Exam.objects.all().order_by("id")
    serializer_class = ExamSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Question model."""
    queryset = Question.objects.select_related("exam").prefetch_related("choices").order_by("id")
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Choice model."""
    queryset = Choice.objects.select_related("question").order_by("id")
    serializer_class = ChoiceSerializer