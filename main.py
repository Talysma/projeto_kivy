'''
Classe MainApp (principal).

Esta classe carrega os outros componentes da aplicação e inicia o app.
'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from appconfig import AppConfig

from telalogin import TelaLogin
from telacadastro import TelaCadastro
from telaperfil import TelaPerfil
from telaeditarperfil import TelaEditarPerfil
from telaabrefoto import TelaAbreFoto

# Classe principal
class MainApp(App):

    '''
    Método de construção da interface.

    Este método instancia um ScreenManager e carrega as outras telas.
    Se existir um token gravado na configuração, significa que o usuário já autenticou antes,
    portanto, irá direto para a tela de perfil.
    '''
    def build(self):
        sm = ScreenManager()
        
        # Se existir token, abre já o perfil. Se não, abre a tela de login.
        if (AppConfig.get_config('token') != None):
            sm.add_widget(TelaPerfil(name='perfil'))
            sm.current_screen.carregar_perfil(AppConfig.get_config('login'))
            sm.add_widget(TelaLogin(name='login'))
        else:
            sm.add_widget(TelaLogin(name='login'))
            sm.add_widget(TelaPerfil(name='perfil'))

        # Carrega as outras telas
        sm.add_widget(TelaCadastro(name='cadastro'))
        sm.add_widget(TelaEditarPerfil(name='editarperfil'))
        sm.add_widget(TelaAbreFoto(name='abrefoto'))

        return sm

# Executa o app
if __name__ == '__main__':
    MainApp().run()
