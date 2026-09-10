from django.contrib import admin
from .models import Exam, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ('text', 'is_correct', 'order')
    extra = 4
    min_num = 2


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ('statement', 'order', 'score')
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'statement', 'order', 'score')
    list_filter = ('exam',)
    search_fields = ('statement',)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__exam')
    search_fields = ('text',)