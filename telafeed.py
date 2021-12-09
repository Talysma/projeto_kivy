

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.graphics import Rectangle,Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button

from botaoimagem import BotaoImagem 


# Classe AppConfig
from appconfig import AppConfig

# Carrega a interface
Builder.load_file('telas/TelaFeed.kv')

'''
Classe TelaFeed
'''
class TelaFeed(Screen):

    # Elementos de interface
    
    layout_postagens = ObjectProperty(None)
   
    '''
    Envia uma requisição do perfil via método GET.

    O parâmetro req_headers contém o Bearer token do usuário autenticado.
    A API do web service deverá retornar o perfil do login informado.
    '''
    def carregar_feed(self):
        UrlRequest(f"{AppConfig.servidor}/api/feed",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.feed_sucesso,
            on_error = self.erro,
        )

    
         

    def feed_sucesso(self, req, resposta):
      if (resposta['status'] == 0):
          postagens = resposta['lista']
          self.layout_postagens.clear_widgets()
          for postagem in postagens:

            layout_quadro =GridLayout()
            layout_quadro.cols=2
              
            layout_curtidas =GridLayout()
            layout_curtidas.cols=2
            layout_curtidas.padding=0


              
              
            layout_postagem =BoxLayout()
            layout_postagem.canvas.add(Color( 255,255,255,0.5 ))
            layout_postagem.canvas.add(Rectangle(size=layout_postagem.size , pos=layout_postagem.pos))

              
            label_data =Label(
              text= f"[ref={postagem['autor_login']}] {postagem['autor']} [/ref] escreveu às {postagem['datahora']}", 
              font_size= '14sp'
            )

            label_data.bind(on_ref_press=self.clique_perfil)    
            label_texto =Label(text=f"{postagem['texto']}\n")


            btn_curtida=BotaoImagem()
            if postagem['curtiu']==True:
                btn_curtida.source='img/curtiu.png'
                btn_curtida.bind(on_press=self.descurtir)
            else:
                btn_curtida.source='img/descurtiu.png'
                btn_curtida.bind(on_press=self.curtir)
            btn_curtida.size=(24,24)
            btn_curtida.id_postagem=postagem['id_post']
            btn_curtida.num_curtidas=postagem['curtidas']
                
            
            label_curtidas=Label(text =f"{postagem['curtidas']} curtida(s).")
            btn_curtida.label_curtidas=label_curtidas

            layout_curtidas.add_widget(btn_curtida)
            layout_curtidas.add_widget(label_curtidas)

            

            foto = AsyncImage(source=f'{AppConfig.servidor}/perfil/avatar/{postagem["autor_login"]}')

             
            layout_postagem.add_widget(label_data)
            layout_postagem.add_widget(label_texto)
            layout_postagem.add_widget(layout_curtidas)

             


            layout_quadro.add_widget(foto)
            layout_quadro.add_widget(layout_postagem)
            self.layout_postagens.add_widget(layout_quadro)


            linha=AsyncImage(source='linha.png')
            linha.height=4
            linha.size_hint_x=1
            
            self.layout_postagens.add_widget(linha)

    def curtir(self,instance):
        UrlRequest(f"{AppConfig.servidor}/api/curtida/{instance.id_postagem}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            method='post',
            on_success = self.curtida_sucesso,
            on_error = self.erro,
        )
        instance.source='img/curtiu.png'
        instance.unbind(on_press=self.curtir)
        instance.bind(on_press=self.descurtir)
        instance.num_curtidas+=1
        instance.label_curtidas.text =f"{instance.num_curtidas}  curtida(s)."

    def descurtir(self,instance):
        UrlRequest(f"{AppConfig.servidor}/api/curtida/{instance.id_postagem}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            method='delete',
            on_success = self.descurtida_sucesso,
            on_error = self.erro,
        )
        instance.source='img/descurtiu.png'
        instance.bind(on_press=self.curtir)
        instance.unbind(on_press=self.descurtir)
        instance.num_curtidas-=1
        instance.label_curtidas.text =f"{instance.num_curtidas}  curtida(s)."

    

    def curtida_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            pass

    def descurtida_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            pass

    '''
    Efetua o tratamento em caso de erro ao efetuar a requisição.
    '''
    def erro(self, req, erro):
        self.lb_login.text = ''
        self.lb_nome.text = 'Erro.'

    def clique_perfil(self,instance,value):
        self.manager.transition.direction = 'right'
        self.manager.current = 'perfil'
        self.manager.current_screen.carregar_perfil(value)