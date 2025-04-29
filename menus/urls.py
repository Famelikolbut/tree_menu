from django.urls import path
from . import views

urlpatterns = [
    path('', views.page, name='home'),
    path('about/', views.page, name='about'),
    path('contacts/', views.page, name='contacts'),
    path('email/', views.page, name='email'),
]