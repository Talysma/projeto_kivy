'''
Classe da Tela de Editar Perfil.

Esta classe é responsável por carregar a interface de edição de perfil e
fazer as requisições ao web service para editar o perfil do usuário autenticado.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode

# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaEditarPerfil.kv')

'''
Classe TelaEditarPerfil
'''
class TelaEditarPerfil(Screen):
    
    # Elementos de interface
    lb_msg = ObjectProperty(None)

    '''
    Envia uma requisição com o novo perfil via método POST.

    O parâmetro req_headers contém o cabeçalho da requisição enquanto
    req_body contém o corpo com os valores do perfil.
    '''
    def enviar(self, senha1, senha2, nome):
        UrlRequest(f'{AppConfig.servidor}/api/perfil/{AppConfig.get_config("login")}',
            on_success = self.alterar_sucesso,
            on_error = self.alterar_erro,
            req_headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain',
                'Authorization': f'Bearer {AppConfig.get_config("token")}',
            },
            req_body = urlencode({
                'senha1': senha1,
                'senha2': senha2,
                'nome': nome,
            }),
        )
    
    '''
    Recebe a resposta da requisição.

    Em caso de sucesso, exibe uma mensagem e retorna à tela de perfil.
    Em caso de erro, exibe uma mensagem vermelha.
    '''
    def alterar_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            # Retorna à tela de perfil
            self.manager.transition.direction = 'right'
            self.manager.current = 'perfil'
            self.manager.current_screen.carregar_perfil(AppConfig.get_config('login'))
        else:
            # Exibe a mensagem de erro na resposta
            self.lb_msg.color = (1, 0.5, 0.5, 1)
            self.lb_msg.text = resposta['msg']
    
    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def alterar_erro(self, req, erro):
        self.lb_msg.color = (1, 0.5, 0.5, 1)
        self.lb_msg.text = 'Erro!'
