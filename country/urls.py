from django.urls import path
from . import views

app_name = 'country'

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('<int:pk>/', views.country_wiki, name='country_wiki'),
    path('<int:pk>/univ', views.country_univ, name='country_univ'),
    path('<int:pk>/qna', views.country_qna, name='country_qna'),
]
