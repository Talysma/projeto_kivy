'''
Classe da Tela de Perfil.

Esta classe é responsável por carregar a interface de perfil com
opções para editar o perfil e sair da conta.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaPerfil.kv')

'''
Classe TelaPerfil
'''
class TelaPerfil(Screen):

    # Elementos de interface
    lb_login = ObjectProperty(None)
    lb_nome = ObjectProperty(None)
    img_perfil = ObjectProperty(None)
    btn_foto = ObjectProperty(None)

    '''
    Envia uma requisição do perfil via método GET.

    O parâmetro req_headers contém o Bearer token do usuário autenticado.
    A API do web service deverá retornar o perfil do login informado.
    '''
    def carregar_perfil(self, login):
        UrlRequest(f"{AppConfig.servidor}/api/perfil/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.perfil_sucesso,
            on_error = self.erro,
        )

       # UrlRequest(f"{AppConfig.servidor}/api/foto/{login}",
            #req_headers = {
               # 'Authorization': f'Bearer {AppConfig.get_config("token")}'
           # },
           # on_success = self.foto_sucesso,
           # on_error = self.erro,
       # )
    
    '''
    Recebe a resposta da requisição do perfil.

    Em caso de sucesso, exibe os dados do perfil.
    Em caso de erro, exibe uma mensagem vermelha.
    '''
    def perfil_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            # Exibe os dados do perfil na interface
            self.lb_login.text = f'[b]{resposta["login"]}[/b]\n'
            self.lb_nome.text = resposta['nome']
        else:
            # Exibe a mensagem de erro na resposta
            self.lb_login.text = ''
            self.lb_nome.text = resposta['msg']

    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def erro(self, req, erro):
        self.lb_login.text = ''
        self.lb_nome.text = 'Erro.'

    '''
    Envia uma requisição de desautenticação via método GET.

    O parâmetro req_headers contém o Bearer token do usuário autenticado.
    A API do web service deverá retornar um status de sucesso e remover
    o token previamente fornecido do banco de dados. O app também deve
    apagar o token no AppConfig.
    '''
    def sair(self):
        UrlRequest(f'{AppConfig.servidor}/api/sair',
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.saida_sucesso,
            on_error = self.erro,
        )
        AppConfig.set_config('token', None)
    
    '''
    Recebe a resposta da requisição de saída.

    Em caso de sucesso, retorna à tela de login.
    '''
    def saida_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            self.manager.transition.direction = 'right'
            self.manager.current = 'login'

    '''
    Recebe a resposta da requisição de foto.

    Em caso de sucesso, atualiza a imagem.
    '''
   # def foto_sucesso(self, req, resposta):
       # if (resposta['status'] == 0):
            # Atualiza a foto na interface
           # self.img_perfil.source = resposta['url']
           # self.img_perfil.reload()
