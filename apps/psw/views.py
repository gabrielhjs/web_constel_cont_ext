from django.shortcuts import render
from bs4 import BeautifulSoup as Bs
import lxml  # É importante para a biblioteca do BeautifulSoap
import re
from time import sleep

from .chromedriver import start_driver


PSW_URL = 'https://www.copel.com/pswweb/paginas/campoatendimentoativacao.jsf'
U_LOGIN = "t290669"
U_SENHA = "Winike$2020"


def view_psw(request):

    driver = start_driver()
    driver.get(PSW_URL)
    driver.implicitly_wait(1)
    usuario = driver.find_element_by_name('j_username')
    usuario.send_keys(U_LOGIN)
    senha = driver.find_element_by_name('j_password')
    senha.send_keys(U_SENHA)
    senha.submit()
    driver.implicitly_wait(1)
    driver.find_element_by_name('form:contrato').send_keys('1390227')
    driver.find_element_by_name('form:j_idt115').click()
    driver.implicitly_wait(2)

    tempo_maximo = 20
    tempo = 0
    carregado = None
    informacoes = []
    dados = []

    while tempo <= tempo_maximo and carregado is None:
        response_info = Bs(driver.page_source, 'lxml')
        informacoes = response_info.find('div', {"id": 'form:painel_content'})
        carregado = informacoes.find_next('span', string='Estado técnico: ')
        informacoes = informacoes.findAllNext('span', {'style': re.compile('.*font-weight:bold.*')})
        sleep(0.2)
        tempo += 0.2

    info_cliente = []

    for i in informacoes:
        info_cliente.append(i.text)

    tempo = 0
    tempo_maximo = 30

    while tempo <= tempo_maximo and dados == []:
        response = driver.page_source
        driver.implicitly_wait(1)
        response_info = Bs(response, 'lxml')
        dados = response_info.find('tbody', {'id': 'form:cli_data'})
        sleep(0.2)
        tempo += 0.2

    dados_cliente = []

    if dados:
        celulas = dados.findAllNext('td')
        rotulos = [
            'Porta:',
            'Estado do Link:',
            'Nível ONT [dB]:',
            'Nível OLT [dB]:',
            'Nível OLT TX:',
            'Número Serial:',
            'Modelo ONT:'
        ]

        for i in range(7):
            dados_cliente.append({'nome': rotulos[i], 'valor': celulas[i].text})

    if not len(info_cliente):
        info_cliente = ['Não foi possível carregar informações']

    if not len(dados_cliente):
        dados_cliente = [{'nome': 'Não foi possível carregar dados'}]

    context = {
        'informacoes': info_cliente,
        'dados': dados_cliente,
    }

    return render(request, 'psw/teste.html', context)
