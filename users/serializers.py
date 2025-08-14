from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import User
from quiz.models import QuizResult
from django.db.models import Avg

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)
    id = serializers.UUIDField(read_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email address already exists.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError("Passwords do not match.")
        validate_password(data.get('password'))
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        if not validated_data.get('username'):
            validated_data['username'] = self.generate_username(validated_data)

        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()

        verification_code = user.create_verify_code()
        self.send_verification_email(user.email, verification_code)
        
        return user

    def generate_username(self, validated_data):
        first_name = validated_data.get('first_name', 'user')
        base_username = f"{first_name}".strip().replace(" ", "").lower()
        unique_username = base_username
        count = 1
        while User.objects.filter(username=unique_username).exists() or self.is_reserved_or_offensive(unique_username):
            unique_username = f"{base_username}_{count}"
            count += 1
        return unique_username

    def is_reserved_or_offensive(self, username):
        reserved_usernames = {'admin', 'root', 'superuser', 'user'}
        return username.lower() in reserved_usernames

    def send_verification_email(self, email, verification_code):
        send_mail(
            'Account Verification',
            f'Your verification code is: {verification_code}',
            'your_email@example.com',
            [email]
        )



class UserSerializer(serializers.ModelSerializer):
    average_quiz_percentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'verified',
            'date_of_birth',
            'photo',
            'bio',
            "first_name",
            "last_name",
            'average_quiz_percentage'
        ]

    def get_average_quiz_percentage(self, obj):
        avg_score = QuizResult.objects.filter(user=obj).aggregate(
            avg=Avg('score')
        )['avg'] or 0
        return round(avg_score, 2)


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'photo', 'bio']
        extra_kwargs = {
            'photo': {'required': False},
            'bio': {'required': False}
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
