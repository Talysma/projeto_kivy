'''
Classe da Tela nova postagem.

'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode

# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaPostar.kv')

'''
Classe TelaPostar
'''
class TelaPostar(Screen):


    lb_msg = ObjectProperty(None)

   
    def postar(self, texto):
        UrlRequest(f"{AppConfig.servidor}/api/postagem",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}',
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'text/plain'

            },
            req_body = urlencode({
                'texto':texto,
            }),
            on_success = self.postar_sucesso,
            on_error = self.erro,
        )

    def postar_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            self.manager.transition.direction = 'right'
            self.manager.current = 'perfil'
            self.manager.current_screen.carregar_perfil(AppConfig.config['login']) 
        else:
            self.lb_msg.text = resposta['msg'] 


    def erro (self, req, erro):
        self.lb_msg.text = 'Erro'

