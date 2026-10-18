"""Serializers for the quiz API.

Design decisions:
- Choices travel nested inside the question because a choice only makes
  sense as part of its question; the client creates and reads a question
  with its choices in a single request.
- The exam travels by identifier (primary key) to avoid repeating the exam
  data in every question; the client fetches the exam from /exams/ if it
  needs it.
"""
from django.db import transaction
from rest_framework import serializers
from quiz.models import Exam, Question, Choice


class NestedChoiceSerializer(serializers.ModelSerializer):
    """Serializer for Choice model when nested inside Question.

    The 'question' field is omitted because the parent question is
    implied by the nesting context.
    """

    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]
        read_only_fields = ["id"]


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for Choice model as a standalone resource (/choices/)."""

    class Meta:
        model = Choice
        fields = ["id", "question", "text", "is_correct"]
        read_only_fields = ["id"]


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for Exam model."""

    class Meta:
        model = Exam
        fields = ["id", "title", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model.

    Choices travel nested inside the question because a choice only makes
    sense as part of its question; the client creates and reads a question
    with its choices in a single request.

    The exam travels by identifier (primary key) to avoid repeating the exam
    data in every question; the client fetches the exam from /exams/ if it
    needs it.
    """

    choices = NestedChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "exam", "statement", "score", "choices"]
        read_only_fields = ["id"]

    def validate_choices(self, value):
        """Validate business rules for question choices.

        - A question needs at least two choices.
        - A question must have exactly one correct choice.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "A question needs at least two choices."
            )
        correct_count = sum(1 for choice in value if choice.get("is_correct"))
        if correct_count != 1:
            raise serializers.ValidationError(
                "A question must have exactly one correct choice."
            )
        return value

    def create(self, validated_data):
        """Create a question with its nested choices."""
        choices_data = validated_data.pop("choices")
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        """Update a question, optionally replacing its choices."""
        choices_data = validated_data.pop("choices", None)
        with transaction.atomic():
            # Update question fields
            instance.statement = validated_data.get("statement", instance.statement)
            instance.score = validated_data.get("score", instance.score)
            instance.exam = validated_data.get("exam", instance.exam)
            instance.save()

            # Replace choices only if explicitly provided
            if choices_data is not None:
                instance.choices.all().delete()
                for choice_data in choices_data:
                    Choice.objects.create(question=instance, **choice_data)
        return instance