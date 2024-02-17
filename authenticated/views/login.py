from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django


def index(request, ):
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_spplit = email.split('@')

        username = email_spplit[0]
        password = request.POST.get('password')

        user = authenticate(
            request, username=username, password=password
        )

        if user:
            login_django(request, user)

            return redirect('index')
        else:

            return redirect('register')
    else:
        return render(
            request,
            'login/login.html'
        )


def logout_(request):
    logout(request)
    return redirect('login')
