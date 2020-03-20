from django.urls import path

from . import views

urlpatterns = [
    path('psw/', views.view_psw, name='login_psw'),
]
