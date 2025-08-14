from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Quiz, QuizResult
from .serializers import QuizSerializer


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.prefetch_related('questions__answers')
    serializer_class = QuizSerializer
    permission_classes = (AllowAny, )


class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.prefetch_related('questions__answers')
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication, )

    def get_serializer_context(self):
        return {'request': self.request}


class QuizCreateView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication, )


class QuizSubmitView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (JWTAuthentication, )

    def post(self, request, quiz_id):
        user_answers = request.data.get('answers', {})
        quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), id=quiz_id)

        question_ids = {str(q.id) for q in quiz.questions.all()}
        if not question_ids.issubset(user_answers.keys()):
            return Response({"error": "Missing answers for some questions"}, status=400)

        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_answer_id = user_answers[str(question.id)]
            selected_answer = question.answers.filter(id=selected_answer_id).first()
            if selected_answer and selected_answer.is_correct:
                score += 1

        score_percent = (score / total_questions) * 100 if total_questions else 0

        QuizResult.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={
                'score': round(score_percent, 2),
                'answers': user_answers
            }
        )

        return Response(
            {
                'score': score,
                'total_questions': total_questions,
                'score_percent': round(score_percent, 2)
            },
            status=status.HTTP_200_OK
        )
