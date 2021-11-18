from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.user_main, name='user_main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/main.html'), name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('rename/', views.rename, name='rename'),
    path('certificate/', views.certificate, name='certificate'),
    path('search_school/', views.school_search, name='search_school'),
    path('users/<str:uidb64>/<str:token>', views.Activate.as_view()),
    path('myquestion/', views.myquestion, name="myquestion"),
    path('mycomment/', views.mycomment, name="mycomment"),
    path('myscraps/', views.myscraps, name="myscraps"),
    path('reset_password/', views.reset_password, name="reset_password"),
]
