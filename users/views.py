from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from .models import User
from .serializers import SignupSerializer, UserSerializer, UpdateProfileSerializer



class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)


class VerifyEmail(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get('id')
        code = request.data.get('code')

        if not user_id or not code:
            return Response({"message": "Missing parameters"}, status=400)

        user = get_object_or_404(User, id=user_id)
        codes = user.verify.filter(
            code=code,
            expiration_time__gte=timezone.now(),
            is_confirmed=False
        )

        if not codes.exists():
            return Response({"message": "Invalid or expired code"}, status=400)

        user.verified = True
        user.save()

        matched_code = codes.first()
        matched_code.is_confirmed = True
        matched_code.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Email verified successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })


class ResendVerificationCode(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_id = request.data.get('id')
        if not user_id:
            return Response({"message": "Missing user ID"}, status=400)

        user = get_object_or_404(User, id=user_id)
        
        if user.verified:
            return Response({"message": "User already verified"}, status=400)

        user.verify.all().delete()
        code = user.create_verify_code()
        self.send_verification_email(email=user.email,verification_code=code)

        return Response({"message": "New verification code sent"})
    
    def send_verification_email(self, email, verification_code):
        send_mail(
            'Account Verification',
            f'Your verification code is: {verification_code}',
            'your_email@example.com',
            [email]
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out successfully."}, status=205)
        except TokenError:
            return Response({"error": "Invalid or expired refresh token."}, status=400)


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class UpdateProfileView(UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
