'''
Classe da Tela de Login.

Esta classe é responsável por carregar a interface de login e fazer
as requisições ao web service para autenticar o usuário.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaLogin.kv')

'''
Classe TelaLogin
'''
class TelaLogin(Screen):

    # Elementos de interface
    lb_msg = ObjectProperty(None)
    txt_login = ObjectProperty(None)

    '''
    Envia uma requisição com os dados de login via método GET.

    A API do web service deverá retornar um token para uso no app.
    '''
    def entrar(self, login, senha):
        UrlRequest(f"{AppConfig.servidor}/api/autenticacao/{login}/{senha}",
            on_success = self.entrar_sucesso,
            on_error = self.entrar_erro,
        )
    
    '''
    Recebe a resposta da requisição.

    Em caso de sucesso, armazena o token no AppConfig e transiciona para
    a tela de perfil.
    Em caso de erro, exibe uma mensagem vermelha.
    '''
    def entrar_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            # Sucesso! Salva o token e o login do usuário.
            AppConfig.set_config('token', resposta['token'])
            AppConfig.set_config('login', self.txt_login.text)

            # Transiciona para a tela de perfil
            self.manager.transition.direction = 'left'
            self.manager.current = 'perfil'
            self.manager.current_screen.carregar_perfil(AppConfig.get_config('login'))
        else:
            # Exibe a mensagem de erro na resposta
            self.lb_msg.color = (1, 0.5, 0.5, 1)
            self.lb_msg.text = resposta['msg']
    
    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def entrar_erro(self, req, erro):
        self.lb_msg.color = (1, 0.5, 0.5, 1)
        self.lb_msg.text = 'Erro ao autenticar.'
