Title: Migrando para o Pelican
Date: 2016-02-11 00:00
Category: Pelican
Tags: python, pelican
status: draft

Depois de um longo hiato, resolvi voltar a dar atenção a esse blog, porém, antes de voltar a escrever, ainda tinha algo que me incomodava bastante, a complexidade do [jekyll](http://blog.getpelican.com/).
Após contribuir com alguns posts no [pythonclub](http://pythonclub.com.br/) descidi que iria migrar para o [Pelican](http://blog.getpelican.com/), pois, além de ser mais simples, o _Pelican_ é feito em python, o que me ajuda bastante em futuras customizações.
<!-- more -->

### O que é Pelican?
Assim como o _Jekyll_ o _Pelican_ é um gerador de site estático simples que não requer um banco de dados ou uma lógica server-side complexa.
Com o pelican, no caso de blogs por exemplo, basta você escrever seus posts em arquivos no formato _markdown_ (ou _rst_ ou _AsciiDoc_) em seu editor favorito e com apenas um comando simples, esses arquivos são convertidos em páginas html estáticas prontas para servir seu blog.

> Contarei aqui como foi o processo de migração do meu antigo blog em jekyll para o pelican.

### Como começar?
Começaremos instalando o Pelican, para isso, crie um virtualenv do python no diretório onde você irá criar seu blog e instale o pelican através o `pip`:
```bash
(venv) $ pip install pelican markdown
```
Com o _Pelican_ instalado, execute o comando `pelican-quickstart` para criar um esqueleto básico do seu blog com o pelican:
```bash
(venv) $ pelican-quickstart
```
Esse comando fará algumas perguntas básicas sobre seu blog, após respondelas, seu blog está praticamente pronto :).

### Como escrever posts?
Com a parte básica do _pelican_ já configurada, agora é hora de escrever um post.
O pelican busca pelo seu conteúdo no diretório `content` dentro da raiz do diretório onde o comando `pelican-quickstart` foi executado, sendo assim, basta criar seus posts nesse diretório.

#### Criando um "Hello World"
Não existem segredos na criação de um post com o pelican, basta criar arquivos no diretório `content` e preencher um cabeçalho mínimo como esse:

```
Title: Titulo do post
Date: Data do post no formato aaaa-mm-dd hh-mm
Category: Categoria do post
```

Sendo assim, nosso _Hello World_ ficaria da seguinte forma:

```
Title: Hello World
Date: 2016-02-11 00:00
Category: Review

Meu primeiro Hello World direto do Pelican \o/
```
### Como gerar o conteúdo?
Gerar o conteúdo estático é a parte mais simples do trabalho, basta executar o comando `pelican "diretório"` e todos arquivos do diretório em questão serão processados:
```bash
(venv) $ pelican content
Done: Processed 1 articles, 0 drafts, 0 pages and 0 hidden pages in 0.70 seconds.
```

### Como vejo o blog no ar?
Agora que todo o conteúdo estático do seu blog já foi gerado, basta iniciar um servidor http no diretório `output` que é o diretório onde o pelican gera os arquivos estáticos.
Para isso, dentro do diretório _output_ basta executar o comando `python -m pelican.server` e abrir o navegar em _http://localhost:8000_.

### TODO: Colocar um print desse hello world funfando

Pronto, seu blog com o Pelican já está no ar.

### Como mudar o tema padrão?
Mudar o tema que será utilizado para gerar o output estático é algo trivial no Pelican, basta você baixar o tema escolhido (você pode escolher alguns disponíveis, no reposítorio [pelican-themes](https://github.com/getpelican/pelican-themes)) e alterar o tema na constante `THEME` do arquivo `pelicanconf.py`.
```python
# pelicanconf.py
THEME = '/diretório/do/tema`
```
Lembrando que os tema são feitos utilizando o [Jinja2](http://jinja.pocoo.org/docs/dev/) como engine de templates, sendo assim, é muito simples customizar os temas ou até mesmo criar um novo.

### Como instalar plugins?
Outra tarefa trivial, basta baixar o plugin (você pode escolher alguns disponíveis no repositório [pelican-plugins](https://github.com/getpelican/pelican-plugins)) e alterar o arquivo `pelicanconf.py` especificando o diretório dos plugins e quais plugins estão ativos:
```python
# pelicanconf.py
PLUGIN_PATHS = ['/diretório/dos/plugins']
PLUGINS = ['plugins', 'ativos']
```

### Como foi a migração do Jekyll para o Pelican?
A migração do Jekyll para o Pelican foi algo extremamente simples, bastou copiar os posts do diretório `source/_post` do jekyll para o diretório `content` do pelican e alterar os metadados dos posts, por exemplo:

* Padrão do Jekyll
```yaml
---
layout: post
title: "Use o cURL"
date: 2014-12-13 01:04:33 -0200
comments: true
categories: [curl]
---
```
* Padrão do Pelican
```markdown
Title: Use o cURL
Date: 2014-12-13 01:04:33
Category: Curl
```
Como decidi usar um tema novo (e não portar o que estava utilizando no jekyll) o resto foram ajustes simples.

**Referências**<br>
[Site Oficial](http://blog.getpelican.com/)<br>
