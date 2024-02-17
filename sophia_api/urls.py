from django.urls import path
from planejamento_semanal import views

urlpatterns = [
    path('usuarios', views.index, name='sophia_users'),
    path('turmas', views.index, name='sophia_class'),
]
