"""Serializers for the quiz API."""
from rest_framework import serializers
from quiz.models import Exam, Question, Choice


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for Exam model."""

    class Meta:
        model = Exam
        fields = ["id", "title", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""

    class Meta:
        model = Question
        fields = ["id", "exam", "statement", "score"]
        read_only_fields = ["id"]


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for Choice model."""

    class Meta:
        model = Choice
        fields = ["id", "question", "text", "is_correct"]
        read_only_fields = ["id"]