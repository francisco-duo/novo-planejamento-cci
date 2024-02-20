import json
from django.shortcuts import render, redirect

TAXONOMIAS = [
    'Lembrar',
    'Entender',
    'Aplicar',
    'Análisar',
    'Avaliar',
    'Elaborar',
    'Interceder'
]


def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            'index/index.html'
        )
    else:
        return redirect('login')


def create_plan(request):
    if request.user.is_authenticated:
        codigo_usuario: str = ''

        turmas: list = []
        disciplina: list = []

        with open('users.json', 'r') as arqv_u:
            arqv_usuarios = json.load(arqv_u)

            for usuario in arqv_usuarios:
                if usuario['email_colaborador'] == request.user.email:
                    codigo_usuario = usuario['codigo_colaborador']
                    break

        with open('turmas.json', 'r') as arqv:
            arqv_turmas = json.load(arqv)

            for turma in arqv_turmas:
                if codigo_usuario in turma['colaborador_codigo']:
                    if turma['turma'] in turmas:
                        pass
                    else:
                        turmas.append(turma['turma'])
                    if turma['disciplinas'] in disciplina:
                        pass
                    else:
                        disciplina.append(turma['disciplinas'])

        return render(
            request, 'planejamento/planejamento.html',
            {
                'turmas': turmas,
                'disciplinas': disciplina,
                'taxonomias': TAXONOMIAS
            }
        )
    else:
        return redirect('login')


def view_plan(request):
    if request.user.is_authenticated:
        from django.shortcuts import HttpResponse
        return HttpResponse("Olá")
    else:
        return redirect('login')


def delete_plan(request):
    ...


def edit_plan(request):
    ...


def publication_plan_classroom(request):
    ...
