from django.db import models
from planejamento_semanal.models.models_turmas import TurmaModel


class DisciplinaModel(models.Model):
    """
        Model Disciplina

        campos:
            - nome_disciplina: varchar()
            - cod_colaborador: varchar()
            - fk_turma: manyToMany()
    """

    nome_disciplina = models.CharField(
        max_length=255
    )
    cod_disciplina = models.CharField(
        max_length=255
    )
    fk_turma = models.ManyToManyField(
        TurmaModel
    )
