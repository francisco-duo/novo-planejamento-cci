from django.urls import path
from authenticated import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.register, name='register'),
    path('logout/', views.logout_, name='logout'),
]
