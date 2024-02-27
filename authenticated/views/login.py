from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib import messages


def index(request, ):
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_split = email.split('@')

        username = email_split[0]
        password = request.POST.get('password')

        try:
            user = authenticate(
                request, username=username, password=password
            )
            if user:
                login_django(request, user)
                return redirect('index')
            else:
                messages.warning(
                    request,
                    'Verifique sua senha'
                )
                messages.warning(
                    request,
                    'Verifique seu email'
                )
                messages.warning(
                    request,
                    'Certifique-se de estar cadastrado'
                )
                return render(
                    request,
                    'login/login.html'
                )
        except Exception:
            messages.warning(
                request,
                'Verifique sua senha'
            )
            messages.warning(
                request,
                'Verifique seu email'
            )
            messages.warning(
                request,
                'Certifique-se de estar cadastrado'
            )
            return render(
                request,
                'login/login.html'
            )
    else:
        return render(
            request,
            'login/login.html'
        )


def logout_(request):
    logout(request)
    return redirect('login')
