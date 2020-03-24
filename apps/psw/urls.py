from django.urls import path

from . import views

urlpatterns = [
    path('psw/login/', views.view_psw_login, name='psw_login'),
    path('psw/contrato/', views.view_psw_contrato, name='psw_contrato'),
]
