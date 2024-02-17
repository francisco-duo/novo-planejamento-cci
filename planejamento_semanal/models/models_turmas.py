from django.db import models


class TurmaModel(models.Model):
    """
        Model Turma

        campos:
            - turma_nome: varchar()
    """

    turma_nome = models.CharField(
        max_length=255, verbose_name='Turma'
    )
