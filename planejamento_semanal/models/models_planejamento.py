from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from planejamento_semanal.models import models_disciplinas, models_turmas

TAXONOMIAS = (
    ('Lembrar',     'Lembrar'),
    ('Entender',    'Entender'),
    ('Aplicar',     'Aplicar'),
    ('Análisar',    'Análisar'),
    ('Avaliar',     'Avaliar'),
    ('Elaborar',    'Elaborar'),
    ('Interceder',  'Interceder'),
)


class PlanejamentoModel(models.Model):
    """
        Model Planejamento

        campos:
            - planejamento_semanal_criador --> ForeingKey(User)
            - planejamento_semanal_turma --> ManyToManyField(Turma)
            - planejamento_semanal_disciplina --> ManyToManyField(Disciplina)
            - planejamento_semanal_taxonomia --> ManyToManyField(Taxonomia)
            - planejamento_semanal_hora_aula --> IntegerField()
            - planejamento_semanal_dt_inicio --> DateTimeField()
            - planejamento_semanal_descricao --> TextField()
            - registro_planejamento_semanal_dt --> DateField()
    """
    planejamento_semanal_criador = models.ForeignKey(
        User, on_delete=models.DO_NOTHING
    )
    planejamento_semanal_turma = models.ManyToManyField(
        models_turmas.TurmaModel
    )
    planejamento_semanal_disciplina = models.ManyToManyField(
        models_disciplinas.DisciplinaModel
    )
    planejamento_semanal_taxonomia = models.CharField(
        max_length=255, blank=True, verbose_name='Taxonomias',
        choices=TAXONOMIAS
    )
    planejamento_semanal_hora_aula = models.IntegerField(
        blank=True, verbose_name='Hora Aula'
    )
    planejamento_semanal_dt_inicio = models.DateTimeField(
        blank=True, verbose_name='Data'
    )
    planejamento_semanal_dt_final = models.DateTimeField(
        blank=True, verbose_name='Data', null=True
    )
    planejamento_semanal_descricao = models.TextField(
        blank=True, verbose_name='Descrição'
    )
    registro_planejamento_semanal_dt = models.DateField(
        default=timezone.now, blank=True, verbose_name='Data de Registro'
    )
    planejamento_semanal_enviado = models.BooleanField(
        blank=True, null=True
    )
    planejamento_semanal_cod_classroom = models.TextField(
        blank=True, null=True
    )
