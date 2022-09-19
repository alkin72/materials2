from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView


def index(request):
    return render(request, 'main/index.html', {'title': ' Главная страница'})


def about(request):
    return render(request, 'main/about.html')


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'
    success_url = reverse_lazy('login')


class LogoutUserView(LogoutView):
    #form_class = AuthenticatForm
    template_name = 'main/login.html'
    success_url = reverse_lazy('login')



