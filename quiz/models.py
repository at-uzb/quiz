from django.conf import settings
from django.db import models


class Quiz(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='quizzes',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='quiz_images/',
        default='images/quiz_default.png'
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        related_name='questions',
        on_delete=models.CASCADE
    )
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class QuizResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='quiz_results',
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz,
        related_name='results',
        on_delete=models.CASCADE
    )
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'quiz'], name='unique_user_quiz_result')
        ]

    def __str__(self):
        return f"{self.user} - {self.quiz} - {self.score}%"
