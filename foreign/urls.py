from django.urls import path
from . import views

app_name = 'foreign'

urlpatterns = [
    path('univ_list',views.univ_list,name='univ_list'),
    path('wiki/<int:pk>',views.wiki,name='wiki'),
    path('wiki/edit_apply/<int:pk>',views.wiki_edit_apply,name='wiki_edit_apply'),

]
