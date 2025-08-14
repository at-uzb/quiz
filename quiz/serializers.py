from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizResult


class PublicAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text']


class PrivateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = PrivateAnswerSerializer(many=True)  

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(question=question, **answer_data) for answer_data in answers_data
        ])
        return question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "answers"]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # <-- writable now
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'owner_username',
            'image_url',
            'questions',
            'completed'
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_completed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            result = QuizResult.objects.filter(user=user, quiz=obj).first()
            if result:
                detailed_results = []
                for question in obj.questions.all():
                    selected_answer_id = result.answers.get(str(question.id))
                    selected_answer = question.answers.filter(id=selected_answer_id).first()
                    correct_answer = question.answers.filter(is_correct=True).first()
                    detailed_results.append({
                        "question": question.question_text,
                        "selected_answer": selected_answer.answer_text if selected_answer else None,
                        "correct_answer": correct_answer.answer_text if correct_answer else None,
                        "is_correct": bool(selected_answer and selected_answer.is_correct),
                    })
                return {
                    "done": True,
                    "score": result.score,
                    "results": detailed_results,
                }
        return {"done": False}

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        owner = self.context["request"].user
        quiz = Quiz.objects.create(owner=owner, **validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return quiz
