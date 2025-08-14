from django.urls import path
from .views import QuizDetailView, QuizSubmitView, QuizListView, QuizCreateView

urlpatterns = [
    path('quizzes/', QuizListView.as_view()),
    path('create-quizz/', QuizCreateView.as_view()),
    path('<int:pk>/', QuizDetailView.as_view()),
    path('<int:quiz_id>/submit/', QuizSubmitView.as_view()),
]

