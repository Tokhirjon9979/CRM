from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('verify_email/', views.VerifyEmailView.as_view(), name="verify_email"),
    path('verification_code/', views.VerificationCodeView.as_view(), name="verification_code"),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name="forgot_password"),
    path('reset_password/', views.ResetPasswordView.as_view(), name="reset_password"),
    path('user_data/', views.UserDataView.as_view(), name="user_data"),
    path('update_profile/', views.UpdateProfileView.as_view(), name='update_profile'),

]