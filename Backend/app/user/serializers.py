from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=5)

    def validate_new_password(self, value):
        """Validate the new password using Django's validators"""
        password_validation.validate_password(value)
        return value


# Reset password
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from django.conf import settings

User = get_user_model()


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def _send_reset_email(self, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Build frontend URL to your reset page
        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}{settings.FRONTEND_RESET_PATH}/{uidb64}/{token}/"

        subject = "Reset your PhlishZil password"
        text_body = (
            f"Hello,\n\nWe received a request to reset your password.\n"
            f"Click the link below to set a new password:\n{reset_url}\n\n"
            "If you didn’t request this, you can safely ignore this email."
        )
        html_body = f"""
        <p>Hello,</p>
        <p>We received a request to reset your password.</p>
        <p><a href="{reset_url}">Click here to set a new password</a></p>
        <p>If you didn’t request this, you can safely ignore this email.</p>
        """

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

    def save(self, **kwargs):
        """
        Do NOT reveal whether the email exists.
        If it exists, send the reset email; otherwise, silently succeed.
        """
        email = self.validated_data["email"].strip().lower()
        try:
            user = User.objects.get(email=email, is_active=True)
            self._send_reset_email(user)
        except User.DoesNotExist:
            pass
        return True


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def save(self, **kwargs):
        uidb64 = self.context.get("uidb64")
        token = self.context.get("token")
        new_password = self.validated_data["new_password"]

        if not uidb64 or not token:
            raise serializers.ValidationError("Invalid reset link.")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, is_active=True)
        except Exception:
            raise serializers.ValidationError("Invalid user.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid or expired reset token.")

        user.set_password(new_password)
        user.save()

        # OPTIONAL (recommended): blacklist outstanding refresh tokens for this user
        # so any stolen/old refresh tokens can’t be used after password reset.
        try:
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
            for outstanding in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=outstanding)
        except Exception:
            # If blacklist app isn’t ready, just skip silently.
            pass

        return user
