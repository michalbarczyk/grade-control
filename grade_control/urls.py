"""grade_control URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path, include

from system import views as system_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', system_views.register, name='register'),
    path('profile/', system_views.profile, name='profile'),
    path('overview/', system_views.overview, name='overview'),
    path('login/', auth_views.LoginView.as_view(template_name='system/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='system/logout.html'), name='logout'),
    path('', include('system.urls')),
]
