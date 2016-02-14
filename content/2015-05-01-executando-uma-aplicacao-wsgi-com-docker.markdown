Title: Executando uma aplicação WSGI com Docker
Date: 2015-05-01 11:05:00
Tags: docker, devops, linux, python
Category: Docker

Já sabemos um pouco sobre o Docker, como ele funciona e como podemos brincar com ele.
Porém, na prática, como podemos conteinerizar nossas aplicações de forma simples e com um bom desempenho?
Veremos nesse post uma _receita de bolo_ de como conteinerizar aplicações WSGI de forma simples com um molde que pode ser reaproveitado sempre que necessário.

<!-- more -->
> Esse post é a continuação do post [Docker, por onde começar](/docker-por-onde-comecar.html), recomendo que faça a leitura do post inicial (caso ainda não tenha feito) antes de prosseguir.

### A aplicação de exemplo
A idéia aqui não é criar uma aplicação complexa e perder tempo explicando como essa aplicação funciona, mas sim, criar uma estrutura que pode servir de molde para outras aplicações que irão rodar em containers (ou não).
Sendo assim, iremos criar a estrutura básica de uma aplicação que poderá ser usada como base para qualquer outra aplicação, independente do Framework, desde que tenha suporte a WSGI.

#### O arquivo RUN.py
O que vai realmente importar para o nosso exemplo é o arquivo `run.py`, nele iremos carregar e disponibilizar o `wsgi` do nosso app.
Basicamente esse será o arquivo que deverá ser chamado quando quisermos colocar nossa aplicação no ar.

```python
from my_app import app


if __name__ == "__main__":
    app.run()
```
O arquivo `run.py` é genérico, ou seja, funciona tanto para aplicações flask, bottle, falcon, etc.
Por exemplo, se estivessemos criando uma aplicação Flask, bastaria ter o seguinte código no arquivo `my_app.py` (ou `my_app/__init__.py`).

```python
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from docker!'
```
Já uma aplicação bottle, poderia ser dessa maneira.
```python
import bottle
from bottle import route


@route('/')
def index():
    return 'Hello from docker!'


app = bottle.default_app()
```
E assim por diante.
Como falei anteriormente, a idéia é não se aprofundar na aplicação, mas sim na arquitetura.

#### Gunicorn
O [Gunicorn](http://gunicorn.org/) é um servidor HTTP dedicado que serve aplicações WSGI, como é o caso de aplicações desenvolvidas com _Flask_, _Django_, _Bootle_, etc.
Com o gunicorn é possível por exemplo executar uma aplicação wsgi com diversos `workers` fazendo assim com que as requisições sejam divididas entre eles e como consequência, tornar a aplicação _mais robusta_.
Utilizaremos o Gunicorn para controlar a instancia de nossa aplicação, com a seguinte _command line_.
```bash
gunicorn -b 0.0.0.0:8000 -w 4 run:app
```
Com o comando acima, estamos liberando o acesso externo para a aplicação, estamos rodando a aplicação com 4 `workers` e finalmente estamos definindo que o objeto WSGI que deverá ser executado é o objeto `app` que se encontra no scritp `run.py`.

> Outra opção ao Gunicorn é o [uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/).

#### Supervisor
O [Supervisor](http://supervisord.org/) é um sistema de que monitora e controla processos unix.
O Supervisor garante que caso nossa aplicação finalize devido a alguma falha, ele se encarregará de subir novamente o processo, assim como subir o processo da aplicação caso o sistema operacional seja reiniciado.
Utilizaremos o Supervisor para controlar nosso processo do _Gunicorn_, com as seguintes configurações.

```
[supervisord]
nodaemon = true

[program:my_app]
command = gunicorn -b 0.0.0.0:8000 -w 4 run:app
directory = /my_app/
autostart= true
autorestart = true
stdout_logfile = /my_app/logs/supervisor.log
redirect_stderr = true
```
Basicamente estamos definindo a _command line_ de nossa aplicação e redirecionando a saída padrão e a saída de erro para um arquivo de log.

### Conteinerizando a aplicação
Finalmente iremos colocar tudo isso dentro de uma imagem do Docker e executar como um container.
Veja um exemplo de como a estrutura do projeto pode ficar.
```
├── my_app
│   └── __init__.py
├── requirements.txt
├── run.py
└── supervisord.conf
```
> Não esqueça de criar o `requirements.txt` com as dependências do seu projeto :)

Para a mágica acontecer, iremos criar nosso `Dockerfile` na raiz do diretório do projeto.

#### Dockerfile
O intuito do Dockerfile será criar uma imagem do Docker com toda a stack que iremos utilizar no projeto, o código fonte da aplicação e uma configuração básica de execução, para que seja possível fácilmente executar a aplicação a partir de um container dessa imagem.

```docker
FROM python:2.7

MAINTAINER Diego Garcia <drgarcia1986@gmail.com>

ADD . /my_app
ADD supervisord.conf /etc/supervisor/conf.d/my_app.conf

WORKDIR /my_app

RUN pip install supervisor gunicorn
RUN pip install -r requirements.txt

RUN mkdir logs
RUN touch logs/supervisor.log

EXPOSE 8000

CMD ["supervisord"]
```
> Já existem as imagens do Python no repostórios padrão do [DockerHub](https://hub.docker.com/) :)

Pronto, já temos tudo que precisamos para containerizar nossa aplicação, sendo assim, `It's party time!`.

### Executando a aplicação via container
#### Criar
Estrutura pronta e Dockerfile pronto, agora é a vez de criar a imagem docker da nossa aplicação, para isso, usaremos o comando `docker build`.

```bash
sudo docker build -t my_app .
```

#### Executar
Após o processo de criação da imagem, basta usar o comando `docker run` para executar o container.
```bash
sudo docker run -d -p 8000:8000 my_app
```
> A opção `-d` está dizendo ao comando que queremos executar o container em background, enquanto que a opção `-p` faz o mapeamento da porta 8000 do container com a porta 8000 local.
> Você pode dar um nome para o container, para isso basta utilizar a opção `--name`.

Com isso nossa aplicação finalmente está no ar em `127.0.0.1:8000`.

#### Listar
Para listar o containers que estão em execução, utilize o comando `docker ps`.
```bash
sudo docker ps
```
#### Parar
E por fim, para parar a execução de um container, existe o comando `docker stop` que espera como parametro o _ID_ (que pode ser obtido através do comando `docker ps`) ou nome do container.
```bash
sudo docker stop 80febff98649
```
### Conclusão
Vimos de uma forma simples e prática como criar um flow de conteinerização de aplicações python wsgi que pode ser reaproveitado sempre que necessário afim de agilizar bastante o processo de configuração e execução da aplicação.
Em um próximo post veremos um pouco sobre o **docker compose** e como fazer o deploy de nossos containers na nuvem.

**Referências**<br>
[Site Oficial](https://www.docker.com/)<br>
[Documentação oficial](http://docs.docker.com/)
