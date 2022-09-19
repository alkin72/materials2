from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),

]