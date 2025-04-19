
from django.urls import path

from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('register/', views.register , name="register"),
 
    path('login/', auth_views.LoginView.as_view(template_name ='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    
    
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='pass_reset/password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='pass_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pass_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pass_reset/password_reset_complete.html'), name='password_reset_complete'),
]

