"""Management command to seed quiz test data."""
from django.core.management.base import BaseCommand
from django.db import transaction
from quiz.models import Exam, Question, Choice


class Command(BaseCommand):
    """Load fixed test data: 2 exams, 12 questions, 36 choices."""

    help = "Seed database with fixed quiz data (idempotent)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding quiz data...")

        with transaction.atomic():
            # Delete existing data in correct order (FK constraints)
            Choice.objects.all().delete()
            Question.objects.all().delete()
            Exam.objects.all().delete()

            # Exam 1: Python Basics (7 questions)
            exam1 = Exam.objects.create(
                title="Python Basics",
                description="Fundamentos de programación en Python"
            )
            self.stdout.write(f"  Created exam: {exam1.title}")

            python_questions = [
                {
                    "statement": "What is a list in Python?",
                    "score": 2,
                    "choices": [
                        ("A mutable ordered sequence", True),
                        ("An immutable tuple", False),
                        ("A key-value mapping", False),
                    ],
                },
                {
                    "statement": "How do you create an empty list?",
                    "score": 1,
                    "choices": [
                        ("[]", True),
                        ("{}", False),
                        ("()", False),
                    ],
                },
                {
                    "statement": "Which method adds an element to the end of a list?",
                    "score": 2,
                    "choices": [
                        ("append()", True),
                        ("insert()", False),
                        ("extend()", False),
                    ],
                },
                {
                    "statement": "What does list comprehension provide?",
                    "score": 3,
                    "choices": [
                        ("Concise way to create lists", True),
                        ("Way to sort lists", False),
                        ("Way to delete lists", False),
                    ],
                },
                {
                    "statement": "What is the output of len([1, 2, 3])?",
                    "score": 1,
                    "choices": [
                        ("3", True),
                        ("2", False),
                        ("4", False),
                    ],
                },
                {
                    "statement": "Which method removes and returns the last item of a list?",
                    "score": 2,
                    "choices": [
                        ("pop()", True),
                        ("remove()", False),
                        ("del", False),
                    ],
                },
                {
                    "statement": "How to check if an item exists in a list?",
                    "score": 1,
                    "choices": [
                        ("item in list", True),
                        ("list.has(item)", False),
                        ("list.contains(item)", False),
                    ],
                },
            ]

            for q_data in python_questions:
                question = Question.objects.create(
                    exam=exam1,
                    statement=q_data["statement"],
                    score=q_data["score"],
                )
                for text, is_correct in q_data["choices"]:
                    Choice.objects.create(
                        question=question, text=text, is_correct=is_correct
                    )

            # Exam 2: Django ORM (5 questions)
            exam2 = Exam.objects.create(
                title="Django ORM",
                description="Object-Relational Mapping en Django"
            )
            self.stdout.write(f"  Created exam: {exam2.title}")

            django_questions = [
                {
                    "statement": "What does QuerySet.filter() return?",
                    "score": 2,
                    "choices": [
                        ("A new QuerySet", True),
                        ("A single object", False),
                        ("A list", False),
                    ],
                },
                {
                    "statement": "Which method retrieves a single object or raises DoesNotExist?",
                    "score": 2,
                    "choices": [
                        ("get()", True),
                        ("filter()", False),
                        ("first()", False),
                    ],
                },
                {
                    "statement": "What is select_related used for?",
                    "score": 3,
                    "choices": [
                        ("Follow ForeignKey relationships in one query", True),
                        ("Follow ManyToMany relationships", False),
                        ("Create database indexes", False),
                    ],
                },
                {
                    "statement": "How to perform a case-insensitive contains lookup?",
                    "score": 1,
                    "choices": [
                        ("__icontains", True),
                        ("__contains", False),
                        ("__iexact", False),
                    ],
                },
                {
                    "statement": "What does prefetch_related optimize?",
                    "score": 3,
                    "choices": [
                        ("ManyToMany and reverse ForeignKey lookups", True),
                        ("Forward ForeignKey lookups", False),
                        ("Database migrations", False),
                    ],
                },
            ]

            for q_data in django_questions:
                question = Question.objects.create(
                    exam=exam2,
                    statement=q_data["statement"],
                    score=q_data["score"],
                )
                for text, is_correct in q_data["choices"]:
                    Choice.objects.create(
                        question=question, text=text, is_correct=is_correct
                    )

        # Summary
        exams_count = Exam.objects.count()
        questions_count = Question.objects.count()
        choices_count = Choice.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f"\nSeeding complete:"
            f"\n  Exams: {exams_count}"
            f"\n  Questions: {questions_count}"
            f"\n  Choices: {choices_count}"
        ))