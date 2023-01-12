from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login / Log Out
    path('login',
         auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('logout',
         auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('signup', views.sign_up, name='signup'),
    path('', views.home, name='home')
]
