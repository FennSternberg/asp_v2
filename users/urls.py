from django.urls import path, include
from .views import login_view, register,account_awaiting_authentication, update_profile
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('account-awaiting-authentication/', account_awaiting_authentication, name='account_awaiting_authentication'), 
    path(
        'password-reset/', 
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html'
        ), 
        name='password_reset'
    ),
    path(
        'password-reset/done/', 
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'password-reset/confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'
    ),
    path(
        'password-reset/complete/', 
        PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
     path('update_profile/', update_profile, name='update_profile'),
]

