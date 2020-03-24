from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .chromedriver import DRIVER
from .forms import FormPswContrato, FormPswLogin


PSW_URL = 'https://www.copel.com/pswweb/paginas/campoatendimentoativacao.jsf'
U_LOGIN = "t290669"
U_SENHA = "Winike$2020"


@login_required
def view_psw_login(request):

    if DRIVER.autenticado:

        return HttpResponseRedirect('/psw/contrato/')

    if request.method == 'POST':
        form = FormPswLogin(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            autenticado = DRIVER.psw_login(request, username, password)

            if autenticado:

                return HttpResponseRedirect('/psw/contrato/')

            else:
                print('ALOOOOOO')
                messages.error(request, 'Usuário e/ou senha incorretos')

    else:
        form = FormPswLogin()

    context = {
        'form': form,
    }

    return render(request, 'psw/psw_login.html', context)


@login_required
def view_psw_contrato(request):

    if not DRIVER.autenticado:

        return HttpResponseRedirect('/psw/login/')

    contrato = request.GET.get('contrato', None)

    form = FormPswContrato(
        initial={'contrato': contrato}
    )

    context = {
        'form': form,
        'button_submit_text': 'Buscar',
    }

    if contrato is not None:

        response = DRIVER.psw_contrato(contrato)

        if response:

            context.update({
                'informacoes': response['informacoes'],
                'dados': response['dados'],
            })

    return render(request, 'psw/teste.html', context)
