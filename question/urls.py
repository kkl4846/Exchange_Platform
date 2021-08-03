from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('create/', views.question_create, name='question_create'),
    path('<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('<int:pk>/delete/', views.question_delete, name='question_delete'),

    path('comment/create/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
