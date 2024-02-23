"""
GOOGLE_UTILS

FILE_NAME -> Caminho para a credencial
SCOPES -> Escopos disponibilizados pelo google
SUBJECT -> Email referente à conta de serviço do admin

Deve retornar uma build para conectar na base de dados do google para acessar
os endpoints referentes ao classroom
"""
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpError

FILE_NAME: str = 'credentials.json'
SCOPES: list = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials'
]
SUBJECT: str = 'francisco.duo@portalcci.com.br'


class ConectarGoogle():
    """
        Conecção com a api do google

        paramentro:
            file_name -> caminho absoluto do arquivo de credencial obtido no
                         google cloud console
            scopes -> endpoints do google
            subject -> conta de email utilizada para criar a credencial no 
                       google cloud console
    """
    def __init__(self):
        self.file_name: str = FILE_NAME
        self.scopes: list = SCOPES
        self.subject: str = SUBJECT

    def credencial(self):
        """
            Credencial

            Tenta criar uma credencial utilizando os dados passado como
            argumento para o objeto. Se o arquivo não existir o método deve
            avisar no consoles, assim como a falta de conecção e a
            indisponibilidade dos serviços oferecidos pelo google.
        """
        try:
            return service_account.Credentials.from_service_account_file(
                filename=self.file_name,
                scopes=self.scopes,
                subject=self.subject
            )
        except HttpError:
            if os.path.exists(self.file_name):
                raise Exception(
                    'O arquivo existe. Verifique a conexão com a internet'
                )
            else:
                raise Exception(
                    f'O arquivo {self.file_name} não existe.'
                )
        except Exception as err:
            raise Exception(err)

    def conectar_classroom(self) -> build:
        """
            Conectar com o classroom

            Depende do método credencial, pois com a credencial gerada é
            possível construir uma build para conectar com o serviço desejado.
        """
        return build("classroom", "v1", credentials=self.credencial())


class Classroom():
    """"""
    def __init__(self, titulo, descricao, curso_nome, professor_email):
        """"""
        self.service: ConectarGoogle.conectar_classroom = ConectarGoogle().conectar_classroom()  # noqa: E501
        self.titulo: str = titulo
        self.descricao: str = descricao
        self.curso_nome: str = curso_nome
        self.professor_email: str = professor_email
        self.course_id: str = ''

    def pegar_id_da_turma(self):
        """"""
        response = self.service.courses().list(
            teacherId=self.professor_email
        ).execute()

        for course in response['courses']:
            if course['name'] == self.curso_nome:
                self.course_id = course['id']

        return self.course_id

    def criar_corpo_da_solicitacao(self):
        """"""
        return {'title': self.titulo, 'description': self.descricao, 'state': 'PUBLISHED'}  # noqa: E501

    def adicionar_material_classroom(self):
        """"""
        return self.service.courses().courseWorkMaterials().create(
            courseId=self.pegar_id_da_turma(),
            body=self.criar_corpo_da_solicitacao()
        ).execute()

    def editar_material_classroom(self, material_id):
        """"""
        return self.service.courses().courseWorkMaterials.patch(
            id=material_id,
            courseId=self.course_id,
            body=self.criar_corpo_da_solicitacao()
        ).execute()


if __name__ == '__main__':
    classroom = Classroom(
        titulo='Teste',
        descricao='Descricao',
        curso_nome='teste_portal_professor',
        professor_email='francisco.duo@portalcci.com.br'
    )

    response = classroom.adicionar_material_classroom()
    print(response)
