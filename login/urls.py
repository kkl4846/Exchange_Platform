from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.user_main, name='user_main'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/main.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
