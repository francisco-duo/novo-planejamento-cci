from django.urls import path
from planejamento_semanal import views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar_planejamento', views.create_plan, name='create_plan'),
    path('visualizar_planejamento', views.view_plan, name='view_plan')
]
