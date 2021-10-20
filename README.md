# Projeto Rede Social

Este é um projeto de uma pequena rede social como parte do aprendizado de desenvolvimento mobile com Python+Kivy.

## Execução no ambiente de desenvolvimento

Para rodar o app no ambiente de desenvolvimento, execute:

```
python3 main.py -m screen:phone_nexus_5,portrait,scale=.4
```

Altere os parâmetros para outros modelos de aparelhos ou escala do tamanho, caso necessário.

## Compilação do APK para Android

O APK pode ser compilado através da ferramenta `buildozer`. Certifique-se de que seu aparelho Android esteja com a depuração USB ativada e conectado a uma porta USB do seu PC. Então, execute:

```
buildozer android debug
```

O `buildozer` também pode fazer o deploy do APK para seu aparelho:

```
buildozer android deploy
```

Instruções sobre como instalar o `buildozer` podem ser encontradas em <https://kivy.org/doc/stable/guide/packaging-android.html>
