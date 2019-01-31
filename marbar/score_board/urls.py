from django.urls import path

from . import views

urlpatterns = [
    path('get_points', views.get_points, name='get_points'),
    path('get_graph', views.get_graph, name='get_graph'),
]