from django.urls import path,include
from . import views

app_name = 'domestic'

urlpatterns = [
    path('', views.univ_list, name='univ_list'),

    path('<int:domestic_id>/wiki/', views.wiki, name='wiki'),
    path('<int:domestic_id>/wiki/edit/apply/', views.wiki_edit_apply, name='wiki_edit_apply'),
    path('<int:domestic_id>/wiki/edit_document/',views.wiki_edit_document, name='wiki_edit_document'),
    path('<int:domestic_id>/wiki/edit_semester/',views.wiki_edit_semester, name='wiki_edit_semester'),
    path('<int:domestic_id>/wiki/edit_scholarship/',views.wiki_edit_scholarship, name='wiki_edit_scholarship'),
    path('<int:domestic_id>/wiki/edit_insurance/',views.wiki_edit_insurance, name='wiki_edit_insurance'),
    
    
    path('<int:domestic_id>/qna/', views.question_list, name='question_list'),
    path('<int:domestic_id>/qna/create/', views.question_create, name='question_create'),
    path('<int:domestic_id>/qna/<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:domestic_id>/qna/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('<int:domestic_id>/qna/<int:pk>/delete/', views.question_delete, name='question_delete'),

    path('<int:domestic_id>/qna/<int:pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:domestic_id>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('<int:domestic_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),


    path('<int:domestic_id>/sister/', views.sister_list, name='sister_list'),


    path('<int:domestic_id>/credit/', views.credit_list, name='credit_list'),
    path('<int:domestic_id>/credit/create', views.credit_create, name='credit_create'),
]
