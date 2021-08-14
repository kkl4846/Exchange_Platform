from django.urls import path
from . import views

app_name = 'country'

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('<int:pk>/', views.country_wiki, name='country_wiki'),

    path('wiki/edit_visa/<int:pk>/', views.wiki_edit_visa, name='wiki_edit_visa'),
    path('wiki/edit_lifestyle/<int:pk>/',
         views.wiki_edit_lifestyle, name='wiki_edit_lifestyle'),
    path('wiki/edit_money/<int:pk>/',
         views.wiki_edit_money, name='wiki_edit_money'),
    path('wiki/edit_culture/<int:pk>/',
         views.wiki_edit_culture, name='wiki_edit_culture'),
    path('wiki/edit_covid_info/<int:pk>/',
         views.wiki_edit_covid_info, name='wiki_edit_covid_info'),

    path('<int:pk>/univ', views.country_univ, name='country_univ'),

    path('<int:country_id>/qna/', views.question_list, name='question_list'),
    path('<int:country_id>/qna/create/',views.question_create, name='question_create'),
    path('<int:country_id>/qna/<int:pk>/',views.question_detail, name='question_detail'),
    path('<int:country_id>/qna/<int:pk>/edit/',views.question_edit, name='question_edit'),
    path('<int:country_id>/qna/<int:pk>/delete/',views.question_delete, name='question_delete'),
    path('<int:country_id>/qna/search/',views.question_search, name='question_search'),

    path('<int:country_id>/qna/<int:pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:country_id>/qna/<int:pk>/comment_update/', views.comment_update, name='comment_update'),
    path('<int:country_id>/qna/<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),

    path('<int:country_id>/qna/<int:pk>/undercomment_create/',views.undercomment_create, name='undercomment_create'),
    path('<int:country_id>/qna/<int:pk>/undercomment_update/',views.undercomment_update, name='undercomment_update'),
    path('<int:country_id>/qna/<int:pk>/undercomment_delete/',views.undercomment_delete, name='undercomment_delete'),

]
