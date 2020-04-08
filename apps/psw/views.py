import requests

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .chromedriver import DRIVER
from .forms import FormPswContrato, FormPswLogin
from my_site.objects import Button


PSW_URL = 'https://www.copel.com/pswweb/paginas/campoatendimentoativacao.jsf'
CONSTEL_WEB_ONT_BAIXA = 'https://constel.herokuapp.com/almoxarifado/cont/api/ont/baixa/'


@login_required
def view_psw_login(request):
    """
        Nesta view é carregado o formulário para preenchimento dos dados de acesso do usuário do sistema PSW.
    :param request: objeto com as informações de requisição do sistema
    :return: returna o redirecionamento para a página de busca de contrato caso o usuário seja autenticado com sucesso
    no sistema da Copel
    """

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
                messages.error(request, 'Usuário e/ou senha incorretos')

    else:
        form = FormPswLogin()

    context = {
        'form': form,
        'callback': 'menu_principal',
        'callback_text': 'Cancelar',
    }

    return render(request, 'psw/psw_login.html', context)


@login_required
def view_psw_contrato(request):
    """
        Nesta view é carregado o forulário para preenchiento do contrato a ser buscado no sistema da Copel.
    Posteriormente esta view exibe os dados encontrados pela busca do contrato.
        À implementar:
        - Posteriormente esta view deve encaminhar as informações obtidas para o sistema principal (Constel.tk) por via
        de http request.
    :param request: objeto com as informações de requisição do sistema
    :return: retorna a própria página com os dados do contrato atualizados
    """

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
            response['dados'].append({'id': 'contrato', 'nome': 'contrato', 'valor': contrato})
            context.update({
                'informacoes': response['informacoes'],
                'dados': response['dados'],
            })

            if len(response['dados']) > 1:
                request.session['dados'] = response['dados']

                button = Button('psw_contrato_baixa', 'Realizar baixa da ONT no sistema')

                context.update({'buttons': [button, ]})

            print(response['dados'])

    return render(request, 'psw/contrato_busca.html', context)


def view_psw_contrato_baixa(request):

    dados = request.session.get('dados', None)

    if dados is None:
        return HttpResponseRedirect('/psw/contrato/')

    headers = {
        "Authorization": 'Token ' + request.user.token.token,
    }
    json = {}
    context = {}

    for dado in dados:
        # print(dado)
        json[dado['id']] = dado['valor']

    json['token'] = request.user.token.token

    try:
        response_url = requests.post(
            CONSTEL_WEB_ONT_BAIXA,
            json=json,
            headers=headers
        )

    except ConnectionError:
        messages.error(request, 'Falha na conexão com o sistema Constel.tk')

        return HttpResponseRedirect('/psw/contrato/baixa/')

    if response_url.status_code == 201:
        matricula = response_url.json()['username']
        nome = response_url.json()['first_name'] + " " + response_url.json()['last_name']

        context.update({
            'matricula': matricula,
            'nome': nome,
        })

        # print(INIT_SPACE + "Ont baixada de:")
        # print(INIT_SPACE + "Matrícula: " + user)
        # print(INIT_SPACE + "Nome: " + user_name)

    elif response_url.status_code == 400:
        errors = response_url.json()['non_field_errors']

        context.update({'errors': errors})

        # for error in errors:
        #     print(INIT_SPACE + "ERRO: " + error)

    else:
        messages.error(request, 'Ocorreu um erro desconhecido, entre em contato com o administrador')
        # print(INIT_SPACE + "Ocorreu um erro desconhecido, entre em contato com o administrador")
        # print(response_url.json())

    print(response_url.json())
    print(context)

    return render(request, 'psw/contrato_baixa.html', context)
