"""API URL configuration for the quiz app."""
from rest_framework.routers import DefaultRouter
from quiz.api_views import ExamViewSet, QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r"exams", ExamViewSet, basename="exam")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"choices", ChoiceViewSet, basename="choice")

urlpatterns = router.urls