from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import (UserLoginForm)
from django.views.generic import TemplateView

app_name = 'account'

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/user/delete_confirmation.html"),
         name='delete_confirm'),
]
