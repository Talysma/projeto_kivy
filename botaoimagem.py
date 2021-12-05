from kivy.uix import behaviors
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage





class BotaoImagem(ButtonBehavior,AsyncImage):
    id_postagem=0
    num_curtidas=0
    label_curtidas=None

