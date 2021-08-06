from django.urls import path
from . import views

app_name = 'country'

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('<int:pk>/', views.country_wiki, name='country_wiki'),

    path('wiki/edit_visa/<int:pk>/', views.wiki_edit_visa, name='wiki_edit_visa'),
    path('wiki/edit_lifestyle/<int:pk>/', views.wiki_edit_lifestyle, name='wiki_edit_lifestyle'),
    path('wiki/edit_money/<int:pk>/', views.wiki_edit_money, name='wiki_edit_money'),
    path('wiki/edit_culture/<int:pk>/', views.wiki_edit_culture, name='wiki_edit_culture'),
    path('wiki/edit_covid_info/<int:pk>/', views.wiki_edit_covid_info, name='wiki_edit_covid_info'),

    path('<int:pk>/univ', views.country_univ, name='country_univ'),
    path('<int:pk>/qna', views.country_qna, name='country_qna'),
]
