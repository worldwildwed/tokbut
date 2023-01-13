from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import account.service as service 

urlpatterns = [
    # Login / Log Out
    path('accounts/login',
         auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('logout',
         auth_views.LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('signup', views.sign_up, name='signup'),
    path('', views.home, name='home')
]

def test_schedule_job():
     print('schedule job @{}'.format(datetime.now()))

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(service.generateTicketQueue, 'interval', minutes=1)
#     scheduler.add_job(test_schedule_job, 'interval', minutes=1)
    scheduler.start()

start_scheduler()