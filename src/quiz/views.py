from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question
from .forms import QuestionForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'quiz/exam_list.html', {'exams': exams})


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, 'quiz/exam_detail.html', {'exam': exam})


def question_create(request):
    exam_id = request.GET.get('exam') or (request.POST.get('exam') if request.method == 'POST' else None)
    exam = get_object_or_404(Exam, pk=exam_id) if exam_id else None

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if exam:
                question.exam = exam
            question.save()

            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                correct_count = sum(
                    1 for f in formset.cleaned_data
                    if f.get('is_correct') and not f.get('DELETE', False)
                )
                if correct_count != 1:
                    question.delete()
                    error_message = 'Debe haber exactamente una opción correcta.'
                    return render(request, 'quiz/question_form.html', {
                        'form': form,
                        'formset': formset,
                        'exam': exam,
                        'error_message': error_message,
                    })
                formset.save()
                return redirect('quiz:exam_detail', pk=question.exam.pk)
            else:
                error_message = 'El formulario de opciones tiene errores. Revíselos.'
                return render(request, 'quiz/question_form.html', {
                    'form': form,
                    'formset': formset,
                    'exam': exam,
                    'error_message': error_message,
                })
        else:
            formset = ChoiceFormSet(request.POST)
            error_message = 'El formulario de la pregunta tiene errores. Revíselos.'
            return render(request, 'quiz/question_form.html', {
                'form': form,
                'formset': formset,
                'exam': exam,
                'error_message': error_message,
            })
    else:
        initial = {'exam': exam} if exam else {}
        form = QuestionForm(initial=initial)
        formset = ChoiceFormSet(instance=Question())

    return render(request, 'quiz/question_form.html', {
        'form': form,
        'formset': formset,
        'exam': exam,
    })