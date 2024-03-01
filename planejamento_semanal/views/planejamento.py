import json
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from planejamento_semanal.models import PlanejamentoSemanal
from planejamento_semanal.google_utils import Classroom

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

        if request.method == 'POST':
            try:
                dt_inicio_str = request.POST.get('date_i1', '')
                dt_final_str = request.POST.get('date_f1', '')

                # Verificar se os campos não estão vazios
                if dt_inicio_str and dt_final_str:
                    # Converter strings para objetos datetime e associar ao fuso horário local
                    dt_inicio = timezone.make_aware(
                        datetime.strptime(dt_inicio_str, '%Y-%m-%d'))
                    dt_final = timezone.make_aware(
                        datetime.strptime(dt_final_str, '%Y-%m-%d'))

                    PlanejamentoSemanal.objects.create(
                        planejamento_semanal_criador=request.user.email,
                        planejamento_semanal_turma=request.POST.get(
                            'badgeValues1').replace('x', ''),
                        planejamento_semanal_disciplina=request.POST.get(
                            'disciplinas1', ''),
                        planejamento_semanal_taxonomia=request.POST.get(
                            'badgeValues2').replace('x', ''),
                        planejamento_semanal_hora_aula=request.POST.get(
                            'hora_aula1', ''),
                        planejamento_semanal_dt_inicio=dt_inicio,
                        planejamento_semanal_dt_final=dt_final,
                        planejamento_semanal_descricao=request.POST.get(
                            'descricao1')
                    )
            except Exception as err:
                print(err)

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


def list_plan(request):
    if request.user.is_authenticated:
        planejamento = PlanejamentoSemanal.objects.filter(
            planejamento_semanal_criador=request.user.email
        ).order_by('-id')
        paginator = Paginator(planejamento, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'planejamento/list_planejamento.html',
                      {'page_obj': page_obj})
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


def edit_plan(request, pk):
    """
        Editar o Planejamento
        parâmetros -> request: Any, pk: int

        Gera e seleciona as turmas e disciplinas em que o usuário é professor.

        A view deve retornar um template 'edit_planejamento.html'.
        Utilizando o parâmetro pk a view obtém os dados do planejamento
        de id <pk>, guarda os dados dos campos do formulário utilizando
        o método POST ao enviar o formulário.

        Deve fazer a conversão de str para o tipo data nos campos
        (data_inicial e data_final).

        Por fim, salva os dados editador pelo usuário no model com id <pk>

        Caso tenha alguma excessão a view deve retornar uma menssagem contendo
        os possíveis erros que o usuáio pode estar cometendo.
    """
    if request.user.is_authenticated:
        planejamento = PlanejamentoSemanal.objects.get(id=pk)

        turma_badge = planejamento.planejamento_semanal_turma.split(',')
        taxonomia_badges = planejamento.planejamento_semanal_taxonomia.split(
            ',')

        data_inicial = planejamento.planejamento_semanal_dt_inicio
        data_final = planejamento.planejamento_semanal_dt_final
        descricao = planejamento.planejamento_semanal_descricao
        hora_aula = planejamento.planejamento_semanal_hora_aula

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

        if request.method == 'POST':
            try:
                planejamento.planejamento_semanal_criador = request.user.email
                planejamento.planejamento_semanal_turma = request.POST.get(
                    'badgeValues1').replace('x', '')
                planejamento.planejamento_semanal_disciplina = request.POST.get(
                    'disciplinas1', '')
                planejamento.planejamento_semanal_taxonomia = request.POST.get(
                    'badgeValues2').replace('x', '')
                planejamento.planejamento_semanal_hora_aula = request.POST.get(
                    'hora_aula1', '')
                planejamento.planejamento_semanal_dt_inicio = data_inicial
                planejamento.planejamento_semanal_dt_final = data_final
                planejamento.planejamento_semanal_descricao = request.POST.get(
                    'descricao1')
                planejamento.save()

                if planejamento.planejamento_semanal_enviado:
                    classroom = Classroom(
                        titulo=f'Planejamento {planejamento.planejamento_semanal_dt_inicio} - {planejamento.planejamento_semanal_dt_final}',
                        descricao=f'{planejamento.planejamento_semanal_taxonomia}\n{planejamento.planejamento.planejamento_semanal_descricao}',
                        curso_nome=turma,
                        professor_email=request.user.email
                    )

                    classroom.editar_material_classroom(
                        material_id=planejamento.planejamento_semanal_cod_classroom,
                        course_id=planejamento.planejamento_semanal_cod_classroom_course
                    )

                return redirect('list_plan')

            except Exception:
                # Messages
                ...
            return redirect('list_plan')

        return render(
            request,
            'planejamento/edit_planejamento.html',
            {
                'turma_badges': turma_badge,
                'taxonomia_badges': taxonomia_badges,
                'turmas': turmas,
                'disciplinas': disciplina,
                'taxonomias': TAXONOMIAS,
                'descricao': descricao,
                'hora_aula': hora_aula,
                'data_inicial': data_inicial,
                'data_final': data_final
            }
        )
    else:
        return redirect('login')


def publication_plan_classroom(request, pk):
    """"""
    if request.user.is_authenticated:
        planejamento = PlanejamentoSemanal.objects.get(id=pk)

        planejamento_turmas = planejamento.planejamento_semanal_turma.split(
            ',')

        for turma in planejamento_turmas:
            classroom = Classroom(
                titulo=f'Planejamento {planejamento.planejamento_semanal_dt_inicio} - {planejamento.planejamento_semanal_dt_final}',
                descricao=f'{planejamento.planejamento_semanal_taxonomia}\n{planejamento.planejamento_semanal_descricao}',
                curso_nome=turma,
                professor_email=request.user.email
            )

            response = classroom.adicionar_material_classroom()

            planejamento.planejamento_semanal_cod_classroom = response.get('id')  # noqa: E501
            planejamento.planejamento_semanal_cod_classroom_course = response.get('courseId')  # noqa: E501
            planejamento.planejamento_semanal_enviado = True
            planejamento.save()

        return redirect('list_plan')
    else:
        return redirect('login')
