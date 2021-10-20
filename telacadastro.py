'''
Classe da Tela de Cadastro.

Esta classe é responsável por carregar a interface de cadastro e fazer
as requisições ao web service para efetuar um cadastro de novo usuário.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode

# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaCadastro.kv')

'''
Classe TelaCadastro.
'''
class TelaCadastro(Screen):

    # Elementos de interface
    lb_msg = ObjectProperty(None)

    '''
    Envia uma requisição com o cadastro via método POST.

    O parâmetro req_headers contém o cabeçalho da requisição enquanto
    req_body contém o corpo com os valores do cadastro.
    '''
    def enviar(self, nome, login, senha1, senha2):
        UrlRequest(f'{AppConfig.servidor}/api/cadastro',
            on_success = self.cadastro_sucesso,
            on_error = self.cadastro_erro,
            req_headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain'
            },
            req_body = urlencode({
                'nome': nome,
                'login': login,
                'senha1': senha1,
                'senha2': senha2,
            }),
        )
    
    '''
    Recebe a resposta da requisição.

    Em caso de sucesso, exibe uma mensagem e retorna à tela de login.
    Em caso de erro, exibe uma mensagem vermelha.
    '''
    def cadastro_sucesso(self, req, resposta):
        if (resposta['status']) == 0:
            # Escreve a mensagem na tela de cadastro
            self.lb_msg.color = (0.5, 1, 0.5, 1)
            self.lb_msg.text = 'Cadastro efetuado!'

            # Transiciona de volta à tela de login, também com mensagem
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'
            self.manager.current_screen.lb_msg.color = (0.5, 1, 0.5, 1)
            self.manager.current_screen.lb_msg.text = 'Cadastro efetuado!'
        else:
            # Exibe a mensagem de erro na resposta
            self.lb_msg.color = (1, 0.5, 0.5, 1)
            self.lb_msg.text = resposta['msg']

    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def cadastro_erro(self, req, erro):
        self.lb_msg.color = (1, 0.5, 0.5, 1)
        self.lb_msg.text = 'Erro ao tentar fazer o cadastro.'
