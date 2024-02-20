import requests

SOPHIA_ACCESS = {
    "usuario": "setape",
    "senha": "setape"
}

POST_AUTH = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Autenticacao"  # noqa: E501
GET_STUDENTS = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos"
GET_STUDENT = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos/"
PUT_STUDENTS = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Alunos/"
GET_CLASSROOM = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Turmas"
GET_SUBJECTS = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Disciplinas"  # noqa: E501
GET_COLABORADOR = "https://portal.sophia.com.br/SophiAWebAPI/3055/api/v1/Colaboradores"  # noqa: E501


# SOPHIA
def connect_sophia():
    access_key = {
        "token": requests.post(
            POST_AUTH, json=SOPHIA_ACCESS
        ).text
    }

    return access_key


def classroom_of_sophia() -> requests:
    return requests.get(
        GET_CLASSROOM, headers=connect_sophia()
    ).json()


def subjects_of_sophia() -> requests:
    return requests.get(
        GET_SUBJECTS, headers=connect_sophia()
    ).json()


def response_users() -> list:
    """
    response_disciplinas

    Returns:
        JsonResponse: arqv.json contendo as informações dos usuários cadastrados
        no sistema de gestão acadêmica sophia.
    """
    response: list = []

    for user in requests.get(GET_COLABORADOR, headers=connect_sophia()).json():
        response.append({
            'codigo_colaborador': user['codigo'],
            'email_colaborador': user['email']
        })

    return response


def http_response_turmas():
    """
    - Vincular o professor e a disciplina na turma

    --> nome 'nome_disciplina'
        --> professoresDisciplinas;
            loop:
                -->
    """
    import json

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


def get_code_of_teacher(email: str) -> str:
    """
    GET_CODE_OF_TEACHER

    Retorna o email do professor ao receber um parametro com o código referente
    ao sistema de gestão escolar Sophia

    parâmetros:
        email: str

    Essa função é responsável por retornar o código correspondente do usuário de
    acordo com a base de dados resgatada do sistema de gestão acadêmica Sophia.
    """
    for user in response_users():
        if email == user['email_colaborador']:
            return str(user['codigo_colaborador'])


if __name__ == '__main__':
    http_response_turmas()
