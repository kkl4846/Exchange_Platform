from django.urls import path
from . import views

app_name = 'country'

urlpatterns = [
    path('', views.country_list, name='country_list'),
]
