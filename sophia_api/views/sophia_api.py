import requests
import json

from django.http import JsonResponse


# Usuário para autenticação na api do sophia
ACESSO_SOPHIA = {"usuario": "setape", "senha": "setape"}

# Endpoints
POST_AUTH = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Autenticacao"  # noqa: E501
GET_STUDENTS = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos"
GET_STUDENT = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos/"
PUT_STUDENTS = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos/"
GET_CLASSROOM = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Turmas"
GET_DISCIPLINA = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Disciplinas"  # noqa: E501
GET_COLABORADOR = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Colaboradores"  # noqa: E501


# Conectando com a api do sophia
def connect_sophia():
    acesso = {
        'token': requests.post(POST_AUTH, json=ACESSO_SOPHIA).text
    }
    return acesso


def http_response_disciplinas(request, ):
    response = []

    for disciplinas in requests.get(GET_DISCIPLINA, headers=connect_sophia()).json():  # noqa: E501
        response.append(disciplinas)

    return JsonResponse(response, safe=False)


def http_response_turmas(request, ):
    """
    - Vincular o professor e a disciplina na turma

    --> nome 'nome_disciplina'
        --> professoresDisciplinas;
            loop:
                -->
    """

    response = []

    for turmas in requests.get(GET_CLASSROOM, headers=connect_sophia()).json():
        for disciplinas in turmas['professoresDisciplinas']:
            response.append(
                {
                    'turma': turmas['nome'],
                    'disciplinas': disciplinas['disciplina']['nome'],
                    'colaborador_nome': [
                        x['nome'] for x in disciplinas['colaboradores']
                    ],
                    'colaborador_codigo': [
                        x['codigo'] for x in disciplinas['colaboradores']
                    ]
                }
            )

    with open(r'turmas.json', 'w') as arqv:
        json.dump(response, arqv)

    return JsonResponse(response, safe=False)


def http_response_usuarios(request, ):
    response = []

    for usuario in requests.get(GET_COLABORADOR, headers=connect_sophia()).json():  # noqa: E501
        response.append(
            {
                'colaborador_codigo': usuario['codigo'],
                'colaborador_nome': usuario['nome'],
                'colaborador_email': usuario['email'],
            }
        )

    with open(r'usuarios.json', 'w') as arqv:
        json.dump(response, arqv)

    return JsonResponse(response, safe=False)
