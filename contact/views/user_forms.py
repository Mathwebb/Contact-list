from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from contact.forms import RegisterForm, RegisterUpdateForm
from contact.models import Contact

def register(request: HttpRequest) -> HttpResponse:
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('contact:register')

    context = {
        'form': form
    }

    return render(
        request,
        'contact/register.html',
        context
    )

def login_view(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('contact:index')
        messages.error(request, 'Login inválido')

    return render(
        request,
        'contact/login.html',
        {
            'form': form
        }
    )

@login_required(login_url='contact:login')
def logout_view(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('contact:login')

@login_required(login_url='contact:login')
def user_update(request: HttpRequest) -> HttpResponse:
    form = RegisterUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = RegisterUpdateForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso')
            return redirect('contact:user_update')

    return render(
        request,
        'contact/user_update.html',
        {
            'form': form
        }
    )
