from django.urls import path
from planejamento_semanal import views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar_planejamento', views.create_plan, name='create_plan'),
    path('meus_planejamentos', views.list_plan, name='list_plan'),
    path('visualizar_planejamento/<int:pk>',
         views.edit_plan, name='view_plan'),
    path('enviar_planejamento_para_classroom/<int:pk>',
         views.publication_plan_classroom, name='class_plan')
]
