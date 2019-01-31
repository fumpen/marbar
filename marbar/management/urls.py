from django.urls import path

from . import views

urlpatterns = [
    path('', views.general_management, name='management_view'),
    path('login/', views.crude_login_view, name='login_view'),
    path('login_post/', views.crude_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_marbar/', views.create_marbar, name='create_marbar'),
    path('create_user/', views.create_user, name='create_user'),
]