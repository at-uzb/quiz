from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignupView,
    VerifyEmail,
    LogoutView,
    UserView,
    UpdateProfileView,
    ProfileView, ResendVerificationCode
)

urlpatterns = [

    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/update/', UpdateProfileView.as_view(), name='update_profile'),  
    path('dashboard/', ProfileView.as_view(), name='profile'),
    path('resend-vcode/', ResendVerificationCode.as_view(), name='resend'),  
    path('<str:username>/', UserView.as_view(), name='public_profile'),
]
