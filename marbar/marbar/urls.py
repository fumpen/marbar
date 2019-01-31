"""marbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from score_board.views import score_board
# from django.contrib.auth import views as auth_views #https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html

urlpatterns = [
    path('', score_board, name='score_board'),
    path(r'admin/', admin.site.urls),
    path(r'management/', include(('management.urls', 'management'), namespace='management')),
    path(r'score_board/', include(('score_board.urls', 'score_board'), namespace='score_board')),
]
