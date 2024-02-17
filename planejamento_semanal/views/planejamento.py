from django.shortcuts import render, redirect

from planejamento_semanal.forms.planejamento import PlanjemantoForm


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
        # POST
        if request.method == 'POST':
            form = PlanjemantoForm(request.POST)

            if form.is_valid():
                form.instance.planejamento_semanal_criador = request.user.email
                form.save()

                return redirect('index')
        else:
            form = PlanjemantoForm()

        return render(
            request,
            'planejamento/create_planejamento.html',
            {'form': form}
        )
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


def edit_plan(request):
    ...


def publication_plan_classroom(request):
    ...
