'''
Classe da Tela de Perfil.

Esta classe é responsável por carregar a interface de perfil com
opções para editar o perfil e sair da conta.
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button


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
    layout_postagens = ObjectProperty(None)
    layout_botoes= ObjectProperty(None)
    btn_perfil= ObjectProperty(None)

    '''
    Envia uma requisição do perfil via método GET.

    O parâmetro req_headers contém o Bearer token do usuário autenticado.
    A API do web service deverá retornar o perfil do login informado.
    '''
    def carregar_perfil(self, login):
        self.login_perfil=login
        UrlRequest(f"{AppConfig.servidor}/api/perfil/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.perfil_sucesso,
            on_error = self.erro,
        )

        UrlRequest(f"{AppConfig.servidor}/api/foto/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.foto_sucesso,
            on_error = self.erro,
        )

        UrlRequest(f"{AppConfig.servidor}/api/postagens/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.postagens_sucesso,
            on_error = self.erro,
    
        )



        self.layout_botoes.clear_widgets()
        if login != AppConfig.get_config('login'):
            
            UrlRequest(f"{AppConfig.servidor}/api/contato/{login}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.contato_sucesso,
            on_error = self.erro,
    
        )
        else:
            btn_editar=Button(text='Editar perfil')
            btn_editar.bind(on_press=self.btn_editar_clique)
           # btn_foto=Button(text='Alterar foto')
            #btn_foto.bind(on_press=self.btn_foto_clique)
            self.layout_botoes.add_widget(btn_editar)
            #self.layout_botoes.add_widget(btn_foto)

            self.img_perfil.bind(on_press=self.btn_foto_clique)

    
    def btn_editar_clique(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'editarperfil'
        self.manager.current_screen.txt_nome.text = self.lb_nome.text
              

    def btn_foto_clique(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'abrefoto'
        self.manager.current_screen.carregar_pasta()



           
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
    def foto_sucesso(self, req, resposta):
      if (resposta['status'] == 0):
            # Atualiza a foto na interface
            self.img_perfil.source = resposta['url']
            self.img_perfil.reload()

    def postagens_sucesso(self, req, resposta):
      if (resposta['status'] == 0):
          postagens = resposta['lista']
          self.layout_postagens.clear_widgets()
          for postagem in postagens:
              
              layout_postagem =BoxLayout()
              #layout_postagem.canvas.add(Color( 255,255,255,0.5 ))
              #layout_postagem.canvas.add(Rectangle(size=layout_postagem.size , pos=layout_postagem.pos))
              label_data =Label(text=postagem['datahora'], font_size= '14sp')
              label_texto =Label(text=f"{postagem['texto']}\n")


              layout_postagem.add_widget(label_data)
              layout_postagem.add_widget(label_texto)
              self.layout_postagens.add_widget(layout_postagem)  


    def contato_sucesso(self, req, resposta):
        if resposta['status']==0:
            btn_desseguir= Button(text='Deixar de seguir')
            btn_desseguir.bind(on_press=self.desseguir)
            self.layout_botoes.add_widget(btn_desseguir)
        else:
            btn_seguir= Button(text='Seguir')
            btn_seguir.bind(on_press=self.seguir)
            self.layout_botoes.add_widget(btn_seguir)


    


       
    def seguir(self,intance):
        UrlRequest(f"{AppConfig.servidor}/api/contato/{self.login_perfil}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
           method='POST',
            on_success = self.seguir_sucesso,
            on_error = self.erro,
        )

    def desseguir(self, intance):
        UrlRequest(f"{AppConfig.servidor}/api/contato/{self.login_perfil}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
           method='DELETE',
            on_success = self.seguir_sucesso,
            on_error = self.erro, 
        )



    def seguir_sucesso(self,req,resposta):
        self.carregar_perfil(self.login_perfil)