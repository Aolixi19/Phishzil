from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views 
from .views import RequestPasswordResetView, ResetPasswordConfirmView,GoogleLoginJWTView

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('me/', views.ManageUserView.as_view(), name='me'),  
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path("password/reset/", RequestPasswordResetView.as_view(), name="password-reset"),
    path("password/reset/confirm/<uidb64>/<token>/",ResetPasswordConfirmView.as_view(), name="password-reset-confirm"),
    path('google-login/', GoogleLoginJWTView.as_view(), name='google-login'),

    
    
    
]
