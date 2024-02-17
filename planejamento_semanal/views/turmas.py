from django.shortcuts import HttpResponse

from planejamento_semanal.models import DisciplinaModel
from planejamento_semanal.models import TurmaModel
from planejamento_semanal.utils import classroom_of_sophia


# VIEW
def adicionar_turmas(request):
    for turma in classroom_of_sophia():
        try:
            TurmaModel.objects.create(
                turma_nome=turma['nome']
            )
        except Exception as err:
            print('Exception: ', err)

    return HttpResponse("Olá")


def adicionar_disciplinas(request):
    for turma in classroom_of_sophia():
        for disciplina in turma['professoresDisciplinas']:
            try:
                turma = TurmaModel.objects.get(
                    turma_nome=turma['nome']
                )

                for info_disciplina in disciplina['colaboradores']:
                    try:
                        DisciplinaModel.objects.create(
                            nome_disciplina=disciplina['disciplina']['nome'],
                            cod_disciplina=info_disciplina['codigo'],
                            fk_turma=turma
                        )

                    except Exception as err:
                        print('disciplina error: ', err)
            except Exception as err:
                print('turma error: ', err)

    return HttpResponse('Disciplinas criadas')
