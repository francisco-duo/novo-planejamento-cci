from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class Instituicao(models.Model):
    """
    Model Instituição

    campos:
        - nome_instituicao --> Charfield()
    """

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

    nome_instituicao = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.nome_instituicao


class Serie(models.Model):
    """
    Model Turma

    campos:
        - nome_serie --> Charfield()
        - instituicao --> ForeignKey(Instituicao)
    """
    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'

    nome_serie = models.CharField(max_length=255, blank=False, verbose_name='Série')  # noqa: E501
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, verbose_name='Instituição')  # noqa:E501

    def __str__(self) -> str:
        return self.nome_serie


class Turma(models.Model):
    """
    Model Turma

    campos:
        - nome_turma --> Charfield()
        - instituicao --> ForeignKey(Instituicao)
    """

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    nome_turma = models.CharField(max_length=100, blank=False, verbose_name='Turma', unique=True)  # noqa: E501
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name='Série', blank=True, null=True)  # noqa:E501

    def __str__(self, ) -> str:
        return self.nome_turma


class Taxonomia(models.Model):
    """
    Model Taxonomia

    campos:
        - nome_taxonomia --> Charfield()
    """

    class Meta:
        verbose_name = 'Taxonomia'
        verbose_name_plural = 'Taxonomias'

    nome_taxonomia = models.CharField(max_length=20, blank=True, verbose_name='Taxonomia')  # noqa: E501

    def __str__(self) -> str:
        return self.nome_taxonomia


class Disciplina(models.Model):
    """
    Model Disciplina

    campos:
        - nome_disciplina --> Charfield()
    """

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    nome_disciplina = models.CharField(max_length=100, blank=True, verbose_name='Disciplina')  # noqa: E501
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, verbose_name='Série', blank=True, null=True)  # noqa:E501

    def __str__(self) -> str:
        return self.nome_disciplina


class PlanejamentoSemanal(models.Model):
    """
    Model Planejamento

    campos:
        - planejamento_semanal_criador --> EmailField()
        - planejamento_semanal_turma --> ManyToManyField(Turma)
        - planejamento_semanal_disciplina --> ManyToManyField(Disciplina)
        - planejamento_semanal_taxonomia --> ManyToManyField(Taxonomia)
        - planejamento_semanal_hora_aula --> Charfield()
        - planejamento_semanal_dt_inicio --> DateTimeField()
        - planejamento_semanal_descricao --> TextField()
        - registro_planejamento_semanal_dt --> DateField()
    """
    planejamento_semanal_criador = models.EmailField(blank=True, verbose_name='Email')  # noqa:E501
    planejamento_semanal_turma = models.CharField(max_length=255, blank=True, verbose_name='Turma')  # noqa:E501
    planejamento_semanal_disciplina = models.CharField(max_length=255, blank=True, verbose_name='Disciplina')  # noqa:E501
    planejamento_semanal_taxonomia = models.CharField(max_length=255, blank=True, verbose_name='Taxonomia')  # noqa:E501
    planejamento_semanal_hora_aula = models.CharField(max_length=255, blank=True, verbose_name='Hora Aula')  # noqa: E501
    planejamento_semanal_dt_inicio = models.DateTimeField(blank=True, verbose_name='Data')  # noqa:E501
    planejamento_semanal_dt_final = models.DateTimeField(blank=True, verbose_name='Data', null=True)  # noqa:E501
    planejamento_semanal_descricao = models.TextField(blank=True, verbose_name='Descrição')  # noqa:E501
    registro_planejamento_semanal_dt = models.DateField(default=timezone.now, blank=True, verbose_name='Data de Registro')  # noqa:E501
    planejamento_semanal_enviado = models.BooleanField(blank=True, null=True, default=False)  # noqa: E501
    planejamento_semanal_cod_classroom = models.TextField(blank=True, null=True)  # noqa: E501
    planejamento_semanal_cod_classroom_course = models.TextField(blank=True, null=True)  # noqa: E501


class RegistroPlanejamentoSemanal(models.Model):
    """
    Model Planejamento

    campos:
        - registro_planejamento_semanal --> Charfield()
        - registro_planejamento_semanal_dt --> DateField()
    """
    registro_planejamento_semanal = models.CharField(blank=False, max_length=255, verbose_name='Email')  # noqa:E501
    registro_planejamento_semanal_dt = models.DateField(default=timezone.now, blank=True, verbose_name='Data de Registro')  # noqa:E501


@receiver(post_save, sender=PlanejamentoSemanal)
def salvar_registro(sender, instance, **kwargs):
    RegistroPlanejamentoSemanal.objects.create(
        registro_planejamento_semanal=instance.planejamento_semanal_criador,
    )


post_save.connect(salvar_registro, sender=PlanejamentoSemanal)