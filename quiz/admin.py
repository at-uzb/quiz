from django.contrib import admin
from .models import Quiz, Question, Answer, QuizResult

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Quiz)
admin.site.register(QuizResult)
admin.site.register(Question, QuestionAdmin)
