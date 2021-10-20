#'''
#Classe da Tela de Abrir Foto.

#Esta classe é responsável por carregar a interface de escolha
#para foto do perfil.
#'''

#from kivy.lang import Builder
#from kivy.uix.screenmanager import Screen
#from kivy.properties import ObjectProperty
#from kivy.network.urlrequest import UrlRequest
#from kivy.utils import platform
#import os

# Classe AppConfig
#from appconfig import AppConfig

# Carrega a interface
#Builder.load_file('telas/TelaAbreFoto.kv')

#'''
#Classe TelaAbreFoto
#'''
#class TelaAbreFoto(Screen):

    # Elementos de interface
    #lb_msg = ObjectProperty(None)
    #escolha_arquivo = ObjectProperty(None)

    #'''
    #Define o diretório padrão do FileChooser de acordo com a plataforma.
    #'''
    #def carregar_pasta(self):
        #if platform == 'linux':
          #  self.escolha_arquivo.rootpath = '/home'
       # elif platform == 'android':
            #self.escolha_arquivo.rootpath = 'C:\\Users'

    #'''
    #Envia uma requisição do perfil via método GET.

   # O parâmetro req_headers contém o Bearer token do usuário autenticado.
   # A API do web service deverá retornar o perfil do login informado.
    #'''
    #def carregar_foto(self, pasta, arquivo):
       # try:
            #arq = open(os.path.join(pasta, arquivo[0]), 'rb')

           # UrlRequest(f'{AppConfig.servidor}/api/foto/{AppConfig.get_config("login")}',
               # req_headers = {
                 #   'Authorization': f'Bearer {AppConfig.get_config("token")}',
               # },
                #req_body = arq.read(),
               # on_success = self.foto_sucesso,
                #on_error = self.erro,
           # )

           # arq.close()
        #except IndexError:
           # self.lb_msg.text = 'Você precisa selecionar um arquivo.'

    #'''
    #Recebe a resposta do envio da foto.

    #Em caso de sucesso, retorna para a tela de perfil.
    #Em caso de erro, exibe uma mensagem de erro.
   # '''
  #  def foto_sucesso(self, req, resposta):
        #if (resposta['status'] == 0):
            # Transiciona para a tela de perfil
           # self.manager.transition.direction = 'right'
           # self.manager.current = 'perfil'
           # self.manager.current_screen.carregar_perfil(AppConfig.get_config('login'))
        #else:
            # Exibe a mensagem de erro na resposta
           # self.lb_msg.text = resposta['msg']

    #'''
    #Efetua o tratamento em caso de erro ao efetuar a requisição.
    #'''
   # def erro(self, req, erro):
        #self.lb_msg = 'Erro.'
