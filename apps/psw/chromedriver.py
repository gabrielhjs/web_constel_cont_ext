from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup as Bs
from django.contrib import messages
import lxml  # É importante para a biblioteca do BeautifulSoap
import re
import os

PSW_URL_LOGIN = 'https://www.copel.com/pswweb/paginas/inicio.jsf'
PSW_URL = 'https://www.copel.com/pswweb/paginas/campoatendimentoativacao.jsf'


class ChromeDriver(object):

    def __init__(self):
        _chrome_options = webdriver.ChromeOptions()
        _chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # _chrome_options.binary_location = "/bin/chromium"
        # _chrome_options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        _chrome_options.add_argument("--headless")
        _chrome_options.add_argument("--disable-dev-shm-usage")
        _chrome_options.add_argument("--no-sandbox")
        _chrome_options.add_argument("--silent-launch")
        self._driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=_chrome_options)
        # self._driver = webdriver.Chrome(executable_path="chromedriver/chromedriver", options=_chrome_options)
        self.autenticado = False

    def psw_login(self, request, username, password):
        self._driver.get(PSW_URL)
        self._driver.implicitly_wait(1)

        try:
            usuario = self._driver.find_element_by_name('j_username')
            usuario.send_keys(username)
            senha = self._driver.find_element_by_name('j_password')
            senha.send_keys(password)
            senha.submit()

        except NoSuchElementException:
            try:
                self._driver.find_element_by_name('form:contrato')

            except NoSuchElementException:
                self.autenticado = False
                messages.error(request, 'Falha ao conectar-se com o PSW')

            else:
                self.autenticado = True

                return self.autenticado

        else:
            self._driver.implicitly_wait(1)

            if self._driver.current_url == 'https://www.copel.com/pswweb/paginas/j_security_check':
                self.autenticado = False

                return self.autenticado

            elif self._driver.current_url == PSW_URL:
                self.autenticado = True

                return self.autenticado

            else:

                return False

    def psw_contrato(self, contrato):

        if not self.autenticado:

            return False

        self._driver.get(PSW_URL)
        self._driver.implicitly_wait(2)

        self._driver.find_element_by_name('form:contrato').send_keys(contrato)
        self._driver.find_element_by_name('form:j_idt115').click()
        self._driver.implicitly_wait(2)

        tempo_maximo = 20
        tempo = 0
        carregado = None
        informacoes = []
        dados = []

        while tempo <= tempo_maximo and carregado is None:
            response_info = Bs(self._driver.page_source, 'lxml')
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
            response = self._driver.page_source
            self._driver.implicitly_wait(1)
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

        return context


DRIVER = ChromeDriver()
