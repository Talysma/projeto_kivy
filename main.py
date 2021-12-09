'''
Classe MainApp (principal).

Esta classe carrega os outros componentes da aplicação e inicia o app.
'''

from os import name
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
 

from appconfig import AppConfig

from telalogin import TelaLogin
from telacadastro import TelaCadastro
from telaperfil import TelaPerfil
from telaeditarperfil import TelaEditarPerfil
from telaabrefoto import TelaAbreFoto
from telapostar import TelaPostar
from telafeed import TelaFeed
from telabusca import TelaBusca



from botaoimagem import BotaoImagem


# Classe principal
class MainApp(App):

    
    sm = ScreenManager()

    '''
    Método de construção da interface.

    Este método instancia um ScreenManager e carrega as outras telas.
    Se existir um token gravado na configuração, significa que o usuário já autenticou antes,
    portanto, irá direto para a tela de perfil.
    '''
    def build(self):
        
        
        # Se existir token, abre já o perfil. Se não, abre a tela de login.
        if (AppConfig.get_config('token') != None):
            self.sm.add_widget(TelaFeed(name='feed'))
            self.sm.current_screen.carregar_feed()
            self.sm.add_widget(TelaLogin(name='login'))
        else:
            self.sm.add_widget(TelaLogin(name='login'))
            self.sm.add_widget(TelaFeed(name='feed'))

        # Carrega as outras telas
        
        
        telaperfil=TelaPerfil(name='perfil')
        telaperfil.carregar_perfil(AppConfig.get_config('login'))
        self.sm.add_widget(TelaCadastro(name='cadastro'))
        self.sm.add_widget(telaperfil)
        self.sm.add_widget(TelaEditarPerfil(name='editarperfil'))
        self.sm.add_widget(TelaAbreFoto(name='abrefoto'))
        self.sm.add_widget(TelaPostar(name='telapostar'))
        self.sm.add_widget(TelaBusca(name='telabusca'))


        return self.sm
name
# Executa o app
if __name__ == '__main__':
    MainApp().run()
