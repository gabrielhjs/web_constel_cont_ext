from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_menu_principal, name='menu_principal'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
]
