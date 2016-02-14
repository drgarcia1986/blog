Title: Docker, por onde começar
Date: 2015-02-15 10:32:26
Tags: docker, devops, linux, python
Category: Docker

Uma das grandes novidades da tecnologia que mais me chamaram a atenção ultimamente é o **Docker**, essa poderosa ferramenta que veio para deixar qualquer devops feliz da vida.
Arrisco dizer que, nos próximos anos, se o Docker não acabar com a virtualização, essa só irá existir em conjunto com o Docker.
O projeto ainda está no começo mas já existem pessoas utilizando em produção.
Entenda um pouco sobre o que é o Docker e como você pode começar a utilizar em seu dia a dia.

<!-- more -->
### Docker
O Docker é uma plataforma open source (escrita em **Go**) que trabalha com o conceito de _containers_.
A ideia do projeto é simples, se você precisa de uma stack com **ubuntu**, **python**, **nginx** e **supervisor** por exemplo, você pode colocar tudo isso em um container e deixar esse container pronto para _subir_ a qualquer hora, sem que seja necessário instalar esses aplicativos novamente.
Pensando dessa forma, o conceito pode se confundir com o conceito de virtualização, porém, o funcionamento é muito diferente.
Enquanto que em uma máquina virtual, possuimos um S.O. completo e isolado, no Docker, aproveitamos o kernel do S.O. hospedeiro, fazendo com isso com que o processo seja muito mais rápido mas sem perder o isolamento dos arquivos e dos processos.

<p align="center">
	<img src="/images/docker_vs_vm.png">
</p>

Para que isso seja possível, o docker utiliza o [Linux Containers](https://linuxcontainers.org/) para ter acesso aos recursos do S.O. e também utiliza o [AuFS](http://aufs.sourceforge.net/) para controlar o sistema de arquivos.

### Instalado o Docker
Chega de conversa fiada, vamos para a prática, afinal, _talk is cheap_.
Para instalar o Docker no ubuntu, basta instalar o pacote `docker.io` através do `apt-get`.

```bash
user@machine:~$ sudo apt-get install docker.io
```
Para confirmar se a instalação foi bem sucedida, utilize o comando `docker version`.

```bash
user@machine:~$ sudo docker version
Client version: 1.0.1
Client API version: 1.12
Go version (client): go1.2.1
Git commit (client): 990021a
Server version: 1.0.1
Server API version: 1.12
Go version (server): go1.2.1
Git commit (server): 990021a
```
> Para utilizar o Docker é necessário acesso de root.

### Criando uma imagem de um container
Agora iremos criar uma imagem de um container do docker para aplicações `WSGI` com Python (_python2.7_, _pip_ e _virtualenv_), Nginx, Gunicorn e Supervisor instalados.
Esse container será baseado na imagem do **Ubuntu**.

#### Ubuntu
As imagens dos containers do docker são armazenadas no **Docker Hub** e podem ser baixadas através do comando `docker pull` (veremos mais sobre o _docker hub_).
Para baixar a imagem do ubuntu, basta executar o comando a seguir.
```bash
user@machine:~$ sudo docker pull ubuntu:14.04
```
> No comando acima, realizamos o download da imagem do ubuntu na _tag_ 14.04.

Para testar se o download da imagem foi bem sucedido, iremos executar uma instrução dentro do container do ubuntu, através do comando `docker run`.
```bash
user@machine:~$ sudo docker run ubuntu:14.04 cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=14.04
DISTRIB_CODENAME=trusty
DISTRIB_DESCRIPTION="Ubuntu 14.04.1 LTS"
```
Essa instrução irá executar o comando `cat /etc/lsb-release` dentro do container do ubuntu.
Se você conseguiu executar esse comando com sucesso, parabéns, você já está utilizando o Docker :).

> Se você tiver algum problema para executar o comando `docker pull` adicione ao final do arquivo `/etc/resolv.conf` a linha `nameserver 8.8.8.8`.

#### Fluxo de criação do container
Antes de prosseguirmos é importante entender o fluxo de criação dos containers.
O Docker é muito semelhante ao **GIT** em termos de fluxo de trabalho.
Por padrão o docker **não** efetiva os comandos que são executados em um container.
Para que as alterações sejam efetivadas é necessário realizar um `commit` dessas alterações.
Isso é excelente para realizar experimentos, pois, imagine que você pode acessar um container, instalar um aplicativo qualquer, realizar diversos teste e sair do container, desta forma as alterações feitas somente serão afetivadas se o comando `docker commit` for executado.

Veremos isso na prática ao instalar nossa stack em nosso container.

#### Criando a Stack
Agora que já temos a imagem base para criar nosso container, podemos dar sequência.
Como iremos instalar diversos aplicativos, faremos do modo mais simples, instalaremos pelo bash do container.
Para iniciar o bash de um container, execute o comando `docker run -t -i IMAGEM /bin/bash`.

```bash
user@machine:~$ sudo docker run -t -i ubuntu:14.04 /bin/bash
root@4e0ba33ccad5:/#
```
Assim será iniciado o bash do container e neste ponto não tem muito segredo, basta instalar os aplicativos.
Começaremos pelos aplicativos que são instalados através do `apt-get` (_python_, _pip_ e _nginx_).

```bash
root@4e0ba33ccad5:/# apt-get update
root@4e0ba33ccad5:/# apt-get install -y python python-pip nginx
```
Com o python e o pip instalado, agora podemos instalar o _virtualenv_, o _gunicorn_ e o _supervisor_.
```bash
root@4e0ba33ccad5:/# pip install virtualenv supervisor gunicorn
```
Para sair do container use o comando `exit`.

#### Realizando commit da alterações

Para que essa alterações sejam efetivadas em nosso container (gerando assim uma nova imagem), devemos executar _commit_.
O comando `docker commit` possui a seguinte sintaxe.
```bash
docker commit [OPÇÕES] CONTAINER [REPOSITORIO]
```
Porém, sabemos que o nome da imagem é `ubuntu:14.04` mas não sabemos a identificação do container que criamos.
Para saber qual é a identificação do ultimo container criado, execute o comando `docker ps -l`.
```bash
user@machine:~$ sudo docker ps -l
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
4e0ba33ccad5        ubuntu:14.04        /bin/bash           22 minutes ago      Exited (0) 11 minutes ago                       focused_mayer
```
Segundo o resultado do comando `docker ps` o ID do nosso container é `4e0b` (só precisaremos dos 4 primeiros digitos).
Sendo assim, para finalmente realizar o commit, utilizaremos o comando a seguir.
```bash
user@machine:~$ sudo docker commit 4e0b wsgi-stack
```
Com o comando acima, estamos criando uma nova imagem chamada `wsgi-stack` com o conteúdo das alterações que realizamos anteriormente.
Para conferir se tudo funcinou corretamente, vamos executar o comando `python --version` em nosso novo container.

```bash
user@machine:~$ sudo docker run wsgi-stack python --version
Python 2.7.6
```
Com isso nossa imagem **wsgi-stack** já está concluída e pronta para o uso, mas antes de efetivamente colocarmos uma aplicações para rodar nela, veremos uma forma mais fácil de criar imagens do docker, através do **Dockerfile**.

### Dockerfile
Um `Dockerfile` é um script que automatiza a criação de imagens do docker.
Podemos simplificar a criação da imagem `wsgi-stack` que criamos anteriormente com o seguinte `Dockerfile`.

```docker
FROM ubuntu:14.04

MAINTAINER Diego Garcia <drgarcia1986@gmal.com>

RUN apt-get update
RUN apt-get install -y python python-pip nginx
RUN pip install virtualenv gunicorn supervisor
```
Para criar a imagem baseado no Dockerfile, basta executar o comando `docker build`.
```bash
user@machine:~$ sudo docker build -t wsgi-stack .
```
> O `.` (ponto) indica que o `Dockerfile` está no mesmo diretório onde o comando `docker build` está sendo executado.

Basicamente o comando acima cria uma imagem chamada `wsgi-stack` baseada no `Dockerfile` que está presente no mesmo diretório.

#### Comandos do Dockerfile
O Dockerfile é uma ferramenta muito poderosa para a criação de imagens do docker.
Veja alguns comandos que podem ser utilizados no Dockerfile.

##### FROM
Primeira instrução, define a imagem base.
```docker
FROM ubuntu14:04
```
##### MAINTAINER
Especifica o autor da imagem.
```docker
MAINTAINER Foo foo@bar.com
```
##### RUN
Equivalente ao comando `docker run`.
```docker
RUN apt-get install python
```
##### ENV
Define uma variável de ambiente.
```docker
ENV PORT=8000
```
##### EXPOSE
Expõe portas.
```docker
EXPOSE 8000
```
##### ADD
Copia arquivos do host hospedeiro para dentro da imagem.
```docker
ADD foo.txt /bar/foo.txt
```
##### ENTRYPOINT
Permite que a imagem seja executada como uma aplicativo (a partir da linha de comando especificada).
```docker
ENTRYPOINT ["python", "app.py"]
```
##### CMD
Comando que será executado quando a execução do container for acionada.
```docker
CMD ["supervisord"]
```

### DockerHub
O DockerHub é uma espécie de _GitHub_ do Docker.
Nele você pode criar uma conta e armazenar suas imagens do Docker, assim como usufluir das imagens de outros usuários.
Em nosso exemplo, utilizamos a imagem do _ubuntu_ que está armazenada no DockerHub, através do comando `docker pull ubuntu` e através do `FROM ubuntu` do Dockerfile.
Assim como no GitHub, o endereço das imagens é sempre `ususário/imagem` com exceção das imagens padrão (como é o caso da imagem do ubuntu).

#### Enviando uma imagem para o Docker Hub
Para enviarmos nossa imagem `wsgi-stack` para o DockerHub, primeiro é necessario [criar uma conta](https://hub.docker.com/account/signup/) no serviço e depois fazer _login_ no aplicativo do Docker.

```bash
user@machine:~$ sudo docker login
Username: drgarcia1986
Password:
Email: drgarcia1986@gmail.com
Login Succeeded
```
Agora para enviar a imagem para o DockerHub, basta utilizar o comando `docker push [IMAGEM]`, porém, o nome da imagem deve serguir o padrão `user/image` e nossa imagem está com o nome de `wsgi-stack`, para resolver essa questão, podemos criar uma `tag` da imagem com o nome no padrão esperado pelo Docker Hub.

```bash
user@machine:~$ sudo docker tag wsgi-stack drgarcia1986/wsgi-stack
```
E finalmente enviar nossa imagem para o DockerHub.
```bash
user@machine~$ sudo docker push drgarcia1986/wsgi-stack
```
Pronto, agora sempre que for preciso um docker com _python2.7_, _pip_, _virtualenv_, _nginx_, _supervisor_ e _gunicorn_, basta fazer um pull da imagem _drgarcia1986/wsgi-stack_.

```bash
user@machine~$ sudo docker pull drgarcia1986/wsgi-stack
```
Em uma segunda parte desse artigo veremos como executar uma aplicação web dentro de um conteiner e como automatizar ainda mais a criação de imagens do Docker através do ~Fig~ **docker compose**.

**Referências**<br>
[Site Oficial](https://www.docker.com/)<br>
[Documentação oficial](http://docs.docker.com/)
