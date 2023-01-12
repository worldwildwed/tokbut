# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from company.models import Company, CompanyUser
# from service import allActiveTicket
import account.service as service 

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff == False:
            user = request.user
            service.allActiveTicket(user)
            return render(request, 'account/home.html', { 'title': 'Hello' })
        else:
            return render(request, 'account/home.html', { 'title': 'Hello Admin' })
    else:
        return redirect('login')
