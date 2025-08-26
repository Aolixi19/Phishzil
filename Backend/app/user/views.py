from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer,ChangePasswordSerializer,ResetPasswordConfirmSerializer,RequestPasswordResetSerializer
from rest_framework.throttling import ScopedRateThrottle
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


#Create user
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

#Authenticate user
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#Manage User profile
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
    
#Change password
class ChangePasswordView(generics.UpdateAPIView):
    """Allow authenticated user to change their password"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RequestPasswordResetView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "If that email exists, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(APIView):
    """
    POST /auth/password/reset/confirm/<uidb64>/<token>/
    Body: { "new_password": "StrongPass123!" }
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset_confirm"
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = ResetPasswordConfirmSerializer(
            data=request.data,
            context={"uidb64": uidb64, "token": token},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )
        
    
User = get_user_model()

class GoogleLoginJWTView(APIView):
    """
    Login/signup with Google ID token and return JWT tokens
    """
    permission_classes = []  # Allow any

    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({"error": "ID token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            # idinfo contains user info
            email = idinfo.get('email')
            name = idinfo.get('name')

            if not email:
                return Response({"error": "Failed to retrieve email from Google"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = name or email.split("@")[0]
                user.save()

            # Issue JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        except ValueError:
            return Response({"error": "Invalid ID token"}, status=status.HTTP_400_BAD_REQUEST)
