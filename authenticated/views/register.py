from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        email: str = request.POST.get('email')

        # Verifica se o e-mail possui o domínio correto.
        if '@portalcci' in email:
            split_email: str = email.split('@')
            username: str = split_email[0]

            password: str = request.POST.get('password')
            confirm_password: str = request.POST.get('confirmPassword')

            messages.warning(
                request,
                'Acesso autorizado somente para o domínio @portalcci.com.br'
            )

            if password == confirm_password:
                register_user = User.objects.create_user(
                    username, email, confirm_password
                )
                register_user.save()

                return redirect('login')
            else:
                messages.warning(
                    request,
                    'Confirmação da senha falhou.'
                )

        else:
            messages.warning(
                request,
                'Somente emails autorizados podem se registrar.'
            )
    else:
        return render(
            request,
            'register/register.html',
        )
