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


if __name__ == '__main__':
    turmas = classroom_of_sophia()
    for i in turmas:
        for c in i['professoresDisciplinas']:
            if c['colaboradores'] != []:
                for x in c['colaboradores']:
                    print(x['codigo'], x['nome'], c['disciplina']['nome'])
