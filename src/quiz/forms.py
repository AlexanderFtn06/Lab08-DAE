from django import forms
from django.forms import inlineformset_factory
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'statement', 'score']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'statement': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=['text', 'is_correct'],
    extra=4,
    can_delete=True,
)