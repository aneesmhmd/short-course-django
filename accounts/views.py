from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(home)

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            print(request.path_info)
            return redirect(home)
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect(login)

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/index.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, 'Incorrect current password')
            return redirect(profile)
        else:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'Password changed succesfully!')
                return redirect(profile)
            else:
                messages.error(request, 'Passwords doesnot match.')
                return redirect(profile)

    return render(request, 'user/change_password.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect(login)