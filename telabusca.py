
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
Builder.load_file('telas/TelaBusca.kv')

'''
Classe TelaFeed
'''
class TelaBusca(Screen):

    # Elementos de interface
    
    lb_mesg= ObjectProperty(None)
    layout_postagens= ObjectProperty(None)
    txt_termo= ObjectProperty(None)
    lb_resultado= ObjectProperty(None)
  

    def buscar(self,termo):
        UrlRequest(f"{AppConfig.servidor}/api/busca/{termo}",
            req_headers = {
                'Authorization': f'Bearer {AppConfig.get_config("token")}'
            },
            on_success = self.busca_sucesso,
            on_error = self.busca_erro,
        )


    def busca_sucesso(self, req, resposta):
        if (resposta['status'] == 0):
            
            
            for postagem in resposta['postagens']:

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
        else:
            # Exibe a mensagem de erro na resposta
            self.lb_msg.color = (1, 0.5, 0.5, 1)
            self.lb_msg.text = resposta['msg']

    def busca_erro(self, req, erro):
        self.lb_msg.color = (1, 0.5, 0.5, 1)
        self.lb_msg.text = 'Erro ao autenticar.'

