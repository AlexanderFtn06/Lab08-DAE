"""Tests for quiz serializers relations (step 4)."""
from django.test import TestCase
from quiz.models import Exam, Question, Choice
from quiz.serializers import QuestionSerializer


class QuestionSerializerRelationsTests(TestCase):
    """Tests for nested choices in QuestionSerializer."""

    def setUp(self):
        """Create an exam for testing."""
        self.exam = Exam.objects.create(title="Test Exam", description="Description")

    def test_create_question_with_nested_choices(self):
        """Create a question with 2 nested choices; verify exam is pk and choices are listed."""
        data = {
            "exam": self.exam.id,
            "statement": "What is REST?",
            "score": 2,
            "choices": [
                {"text": "An architectural style", "is_correct": True},
                {"text": "A language", "is_correct": False},
            ],
        }
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        question = serializer.save()

        # Check that 2 choices were created and linked to the question
        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(question.choices.count(), 2)

        # Verify output structure
        output = QuestionSerializer(question).data
        self.assertEqual(output["exam"], self.exam.id)
        self.assertIsInstance(output["choices"], list)
        self.assertEqual(len(output["choices"]), 2)
        for choice in output["choices"]:
            self.assertIn("id", choice)
            self.assertIn("text", choice)
            self.assertIn("is_correct", choice)
            self.assertNotIn("question", choice)

    def test_partial_update_without_choices_keeps_choices(self):
        """Partial update with only statement keeps existing choices unchanged."""
        # Create initial question with choices
        question = Question.objects.create(
            exam=self.exam, statement="Original statement", score=3
        )
        choice1 = Choice.objects.create(
            question=question, text="Choice A", is_correct=True
        )
        choice2 = Choice.objects.create(
            question=question, text="Choice B", is_correct=False
        )

        # Partial update: only statement
        serializer = QuestionSerializer(
            question, data={"statement": "Updated statement"}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_question = serializer.save()

        # Verify statement changed
        self.assertEqual(updated_question.statement, "Updated statement")

        # Verify choices are kept with same IDs
        self.assertEqual(Choice.objects.count(), 2)
        updated_choices = list(updated_question.choices.order_by("id"))
        self.assertEqual(updated_choices[0].id, choice1.id)
        self.assertEqual(updated_choices[0].text, "Choice A")
        self.assertEqual(updated_choices[1].id, choice2.id)
        self.assertEqual(updated_choices[1].text, "Choice B")

    def test_update_with_choices_replaces_them(self):
        """Full update with new choices replaces the old ones."""
        # Create initial question with choices
        question = Question.objects.create(
            exam=self.exam, statement="Original", score=1
        )
        Choice.objects.create(question=question, text="Old A", is_correct=True)
        Choice.objects.create(question=question, text="Old B", is_correct=False)

        # Full update with new choices
        data = {
            "exam": self.exam.id,
            "statement": "New statement",
            "score": 5,
            "choices": [
                {"text": "New C", "is_correct": True},
                {"text": "New D", "is_correct": False},
                {"text": "New E", "is_correct": False},
            ],
        }
        serializer = QuestionSerializer(question, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_question = serializer.save()

        # Verify old choices are gone, new ones exist
        self.assertEqual(Choice.objects.count(), 3)
        new_choices = list(updated_question.choices.order_by("id").values_list("text", flat=True))
        self.assertEqual(new_choices, ["New C", "New D", "New E"])

        # Verify statement and score updated
        self.assertEqual(updated_question.statement, "New statement")
        self.assertEqual(updated_question.score, 5)