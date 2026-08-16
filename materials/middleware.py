from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

class RestrictUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')
        register_url = reverse('register')

        # Список путей, куда разрешено заходить без авторизации
        allowed_paths = [login_url, register_url]

        if not request.user.is_authenticated and request.path not in allowed_paths:
            # Проверяем, есть ли вообще пользователи в базе данных
            # Если пользователей ноль — никто еще не зарегистрировался, отправляем на регистрацию
            if User.objects.exists():
                return redirect(login_url)
            else:
                return redirect(register_url)

        response = self.get_response(request)
        return response
