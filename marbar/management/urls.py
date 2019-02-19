from django.urls import path

from . import views

urlpatterns = [
    path('', views.general_management, name='management_view'),
    path('login/', views.crude_login_view, name='login_view'),
    path('login_post/', views.crude_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('create_marbar/', views.create_marbar, name='create_marbar'),
    path('create_user/', views.create_user, name='create_user'),
    path('update_marbar/', views.update_marbar, name='update_marbar'),
    path('activate_marbar/', views.activate_marbar, name='activate_marbar'),
    path('events/', views.events_view, name='events'),
    path('delete_event/', views.delete_event, name='delete_event'),
]

