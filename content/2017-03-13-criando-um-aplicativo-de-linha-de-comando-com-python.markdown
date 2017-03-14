Title: Criando Um Aplicativo De Linha De Comando Com Python
Date: 2017-03-13 22:00
Category: Python
Tags: python, argparse

Com certeza você já uso algum aplicativo de linha de comando, seja dos mais simples (como por exemplo o _echo_),
ou dos mais sofisticados (como é o caso do [cURL](/2014/12/13/use-o-curl/)).
O fato é, todo programador deveria criar pelo menos uma vez um aplicativo de linha de comando, seja para fins de estudo,
ou até mesmo para se tornar uma grande ferramenta. Com python, criar aplicativos de linha de comando é algo muito simples e produtivo.

<!-- more -->

## Hello World
Antes de nos aprofundarmos no assunto, faremos um simples `Hello World` utilizando o módulo `argparse` que é built-in do python.

```python
# cli.py
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('name', help='say your name')

args = parser.parse_args()
print('Hello {}'.format(args.name))
```
Resumindo o código anterior, criamos um `parser` e nesse _parser_ adicionamos um _argumento posicional_ (o argumento `name`).
Depois convertemos os argumentos da linha de comando no objeto `args` e mostramos uma mensagem utilizando o valor passado para o
argumento _name_.
O resultado será o seguinte:

```bash
$ python cli.py World
Hello World
```
Pode parecer mais complicado do que simplesmente recuperar os valores de [`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv),
porém, é algo muito mais poderoso.
Um exemplo disso é o fato de que, esse código da forma como está, já possui um _help_ bem intuitivo dos possíveis comandos aceitos:

```
$ python cli.py -h
usage: cli.py [-h] name

positional arguments:
  name        say your name

optional arguments:
  -h, --help  show this help message and exit
```

## Um pouco sobre o Argparse
O `argparse` é um módulo que foi adicionado a standard library do python a partir da versão 2.7 substituindo seu antecessor, o módulo `optparse`.
Ele foi projetado para criar aplicativos de linha de comando de forma amigável e descomplicada.

### O parser

O principal componente do módulo _argparse_ é a classe `ArgumentParser`.
A partir de uma instância de _ArgumentParser_ é possível determinar o comportamento de linha de comando do aplicativo.
Na criação do parser é possível informar alguns parâmetros relativos ao aplicativo, sendo que alguns deles servem para customizar
a mensagem de _help_ gerada automaticamente, como é o caso do parâmetro `description`:

```python
>>> from argparse import ArgumentParser
>>> parser = ArgumentParser(description='Powerful command-line tool')
>>> parser.parse_args(['-h'])
usage: [-h]

Powerful command-line tool

optional arguments:
  -h, --help  show this help message and exit
```
Note que é possível informar para o parser os argumentos que ele deve parsear, através do método `parse_args`.
Esse método espera uma lista de strings como parâmetro e caso essa não seja informada, recupera a lista de
argumentos através do `sys.argv`, ou seja, os argumentos de linha de comando.

### Argumentos
Com vimos no primeiro exemplo, é possível adicionar argumentos ao parser, sejam eles _posicionais_ (e obrigátorios),
ou _opcionais_.

#### Argumentos posicionais
Os argumentos posicionais, são argumentos obrigatórios que devem ser informados na ordem em que foram declarados.
Veja um exemplo de uma simples soma feita através da linha de comando:

```python
# cli.py
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('first_number', type=int)
parser.add_argument('second_number', type=int)

args = parser.parse_args()
print('{} + {} = {}'.format(
    args.first_number,
    args.second_number,
    args.first_number + args.second_number
))
```
O exemplo de uso do código anterior seria algo como:
```
$ python cli.py 2 5
2 + 5 = 7
```
> Não se preocupe com o `type` no exemplo, veremos o que isso significa mais adiante

#### Argumentos opcionais
Os argumentos opcionais são declarados com um ou dois hífens no prefixo do nome (e.g. _-f_, _--foo_) e não
dependem de uma posição especifica para serem informados.
Usando o exemplo anterior, vamos adicionar um argumento opcional para determinar se o output do comando
deve ou não ser verboso:

```python
# cli.py
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('first_number', type=int)
parser.add_argument('second_number', type=int)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()
result = args.first_number + args.second_number
if args.verbose:
    print('{} + {} = {}'.format(
        args.first_number,
        args.second_number,
        result
    ))
else:
    print(result)
```
Desta forma, possibilitamos saidas diferentes da nossa aplicação de acordo com a presença ou não do
argumento `--verbose`.

```
$ python cli.py 2 5
7
$ python t.py 2 5 --verbose
2 + 5 = 7
```
> Não se preocupe com o `action` no exemplo, veremos o que isso significa mais adiante

Podemos simplificar aindas mais o argumento _--verbose_ criando uma opção encurtada dele.
O método `add_argument` do `ArgumentParser` aceita uma lista de nomes do argumento, sendo assim,
basta adicionar as opções na criação do argumento:

```python
parser.add_argument('-v', '--verbose', action='store_true')
```
E inclusive, essa alteração já reflete no _help_ da aplicação:

```
$ python cli.py -h
usage: cli.py [-h] [-v] first_number second_number

positional arguments:
  first_number
  second_number

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

Vale ressaltar que essa opção só faz sentido para argumentos opcionais.

### Types
Por padrão, o valor de todos os argumentos são interpretados como _string_, porém, é possível determinar um tipo
para esses valores, através do parametro `type` do método `add_argument` como já vimos anteriormente.<br>
Ao determinar um _type_ para um argumento, será executado um _type-checking_ no momento do *parse_args()* para garantir
que o valor do argumento é do tipo especificado:

````python
>>> from argparse import ArgumentParser
>>> parser = ArgumentParser()
>>> parser.add_argument('number', type=int)
>>> args = parser.parse_args(['a'])
usage: [-h] number
: error: argument number: invalid int value: 'a'
```
Qualquer _callable_ pode ser usado como type, pontencializando ainda mais o uso de tipos nos argumentos, e.g.

```python
# cli.py
import argparse


def odd(n):
    n = int(n)
    if n % 2 == 1:
        return n
    raise argparse.ArgumentTypeError('{} is not an odd number'.format(n))


parser = argparse.ArgumentParser()
parser.add_argument('odd_number', type=odd)
args = parser.parse_args()
```
Neste exemplo, se pasarmos um numero par para o argumento `odd_number` teremos uma mensagem
de erro indicando que esse numero não é um numero impar.

```
$ python cli.py 2
usage: [-h] odd_number
: error: argument odd_number: 2 its not an odd number
```

### Actions
É possível determinar ações para determinados argumentos sendo a mais comum a ação `store` que
basicamente armazena o valor passado para o argumento. Esta é a ação default para qualquer argumento
caso outro tipo de ação não seja informado.<br>
Existem outros tipos de ações, veremos algumas delas.

#### store_true
A action `store_true` basicamente armazena o valor `True` caso o argumento
seja informado (como vimos anteriormente no exemplo do argumento _--verbose_).

#### append
A action `append` armazena uma lista dos valores passados para o mesmo argumento, e.g.:
```python
>>> from argparse import ArgumentParser
>>> parser = ArgumentParser()
>>> parser.add_argument('--file', action='append')
>>> parser.parse_args('--file 1.txt --file 2.txt --file 3.txt'.split())
Namespace(file=['1.txt', '2.txt', '3.txt'])
```

#### count
A action `count` armazena um contador de vezes em que um argumento foi usado
(útil para determinar niveis de verbosidade), e.g.:
```python
>>> from argparse import ArgumentParser
>>> parser = ArgumentParser()
>>> parser.add_argument('--verbose', '-v',  action='count')
>>> parser.parse_args(['-vvvv'])
Namespace(verbose=4)
```

## Casos mais complexos
Normalmente, no desenvolvimento de um aplicativo _cli_ acabamos tendo que lidar com casos mais complexos,
e não somente um comando simples com alguns parâmetros. Esses aplicativos tendem a crescer
e lidar com outros subcomandos, como por exemplo o **git** (_add_, _commit_, _branch_, etc):

Iremos criar um aplicativo simples com dois subcomandos, o subcomando `read` e o subcomando `write`.

A melhor maneira de lidar com subcomandos é criar `SubParsers` especificos para cada
comando que o aplicativo irá lidar.

### SubParsers
Subparsers são parsers independentes, com suas próprias caracteristicas
mas que deviram de um parser principal.
Vamos começar nosso aplicativo de exemplo criando seu parser principal e seus dois
subparsers:

```python
# cli.py
from argparse import ArgumentParser


parser = ArgumentParser()

subparsers = parser.add_subparsers()
r_parser = subparsers.add_parser('read', help='Commands to read data')
w_parser = subparsers.add_parser('write', help='Commands to write data')

parser.parse_args()
```

Se dermos uma olhada no _help_ gerado pelo python, já veremos instruções de uso
para os subcomandos:

```
$ python cli.py -h
usage: cli.py [-h] {read,write} ...

positional arguments:
  {read,write}
    read        Commands to read data
    write       Commands to write data

optional arguments:
  -h, --help    show this help message and exit
```

Iremos agora incrementar um pouco mais nosso aplicativo adicionando argumentos para cada
subcomando:
```python
# cli.py
from argparse import ArgumentParser

parser = ArgumentParser()
subparsers = parser.add_subparsers(help='Sub commands')

r_parser = subparsers.add_parser('read', help='Commands to read data')
r_parser.add_argument('origin', help='File origin')
r_parser.add_argument('--head', type=int, default=0, help='Read only N lines')

w_parser = subparsers.add_parser('write', help='Commands to write data')
w_parser.add_argument('destination', help='Destination file')
w_parser.add_argument(
    '--upper',
    action='store_true',
    help='Write all in UPPERCASE'
)

if __name__ == '__main__':
    args = parser.parse_args()
```
Agora é possível ter um help geral do aplicativo e um help para cada subcomando:

```
$ python cli.py -h

usage: cli.py [-h] {read,write} ...

positional arguments:
  {read,write}  Sub commands
    read        Commands to read data
    write       Commands to write data

optional arguments:
  -h, --help    show this help message and exit
```

```
$ python cli.py read -h

usage: cli.py read [-h] [--head HEAD] origin

positional arguments:
  origin       File origin

optional arguments:
  -h, --help   show this help message and exit
  --head HEAD  Read only N lines
```

```
$ python cli.py write -h

usage: cli.py write [-h] [--upper] destination

positional arguments:
  destination  Destination file

optional arguments:
  -h, --help   show this help message and exit
  --upper      Write all in UPPERCASE
```

### set_defaults
Um problema ao se utilizar subparsers é que ao executar o `parser.parser_args()` não
é possível determinar qual subcomando foi requisitado, somente os argumentos do
subparser:

```
$ python cli.py read foo.txt --head 2
Namespace(head=2, origin='foo.txt')
```
Para contornar esse comportamento, é possível determinar valores default para
um subparser através do método `set_default`, que espera um conjunto de argumentos nomeados (_**kwargs_):

```python
# cli.py
r_parser.set_defaults(command='read')
...
args = parser.parse_args()
print('subcommand: ', args.command)
```

Para o exemplo anterior, ao chamar o _cli.py_ na linha de comando passando o subcomando `read`
teriamos a seguinte saida:

```
$ python cli.py read foo.txt
subcommand: read
```

### Criando handlers para os subparsers
Conhecendo esse truque e sabendo que o valor default pode ser de qualquer tipo (inclusive um callable),
podemos criar _handlers_ para os nossos subcommands.<br>
Vamos mudar nosso código de exemplo adicionado duas funções, a função `read` e a função `write`:

```python
def read(args):
    print('call read with: {}'.format(args))


def write(args):
    print('call write with: {}'.format(args))
```

Agora iremos usar essas funções como um valor default em nossos subparser:

```python
r_parser.set_defaults(handler=read)
w_parser.set_defaults(handler=write)
```
E por fim, iremos usar essas funções após a leitura dos argumentos da linha de comando:

```python
args = parser.parse_args()
args.handler(args)
```

Ao executarmos nosso cli passando um subcomando, podemos ver que a saída do comando indica
que nosso _handler_ foi chamado:

```
$ python cli.py write foo.txt --upper
call write with: Namespace(destination='foo.txt', handler=<function write at 0x100de9140>, upper=True)
```

Isso abre a possíbilidade de criar aplicativos realmente complexos de
forma simples e organizada.

### Testando Parsers
> “I don’t care if it works on your machine! We are not shipping your machine!” — Vidiu Platon.

Software sem testes é um software que não deve ser entregue, ou seja, é um software incompleto.
Já sabemos como criar complexas soluções de aplicativos de linha de comando, só nos falta saber
como criar testes para essa aplicações.<br>
Usando o _ArgumentParser_  do python não existe muitos mistérios em como realizar os testes,
para utilizar o método `parse_args()` e verificar a forma como os argumentos foram processados:

```python
>>> from argparse import ArgumentParser
>>> parser = ArgumentParser()

>>> subparser = parser.add_subparsers()
>>> x_parser = subparser.add_parser('x')
>>> x_parser.set_defaults(foo='bar')

>>> args = parser.parse_args(['x'])
>>> assert args.foo == 'bar'
>>> assert args.foo == 'x'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

> Algumas quebras de linha foram adicionadas para melhorar a leitura

Você pode tranquilamente utilizar esse recurso dentro da sua suite de testes.

## Distribuindo seu aplicativo
Com o aplicativo já escrito (e devidamente testado), chegou a hora de distribuir para o mundo.
Não irei entrar em detalhes sobre como prepara o arquivo `setup.py` de forma correta
(talvez em outro post), porém irei comentar sobre uma configuração especifica, os `entry_points`.

### Entrypoint
Existem diferentes tipos de entrypoints disponíveis para serem usados, em nosso exemplo iremos
usar o mais comum deles, o `console_script`, com isso, iremos determinar como a nossa aplicação
deverá ser chamada na linha de comando após a instalação:

```python
# setup.py
from setuptools import setup, find_packages

author_name = 'Diego Garcia'
author_email = 'drgarcia1986@gmail.com'

setup(
    name='cli',
    version='0.0.1',
    description='Cool cli',
    long_description='Cool cli from http://www.diego-garcia.info/,
    url='https://github.com/drgarcia1986/cli',
    author=author_name,
    author_email=author_email,
    maintainer=author_name,
    maintainer_email=author_email,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='cli',
    download_url='https://github.com/drgarcia1986/cli/archive/master.zip',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    entry_points={'console_scripts': ['cli = cli:main']},
    platforms='windows linux',
)
```

O detalhe importante fica por conta da linha `entry_points={'console_scripts': ['cli = cli:main']}`,
onde determinamos que o _entry point_ de _console script_ da nossa aplicação, será
a função _main_ dentro do arquivo _cli_, para quando a aplicação for chamada como
_cli_ na linha de comando. <br>
Essa função _main_ nada mais é do que uma função que chama o método *parser_args()*, e.g.:

```python
def main():
    args = parser.parse_args()
    args.handler(args)
```

Pronto, ao realizar a instalação da aplicação podemos utiliza-la na linha de comando apenas
chamando o comando `cli`:

```python
$ cli -h

usage: cli [-h] {read,write} ...

positional arguments:
  {read,write}  Sub commands
    read        Commands to read data
    write       Commands to write data

optional arguments:
  -h, --help    show this help message and exit
```

## Third party libs
Existem algumas bibliotecas opensource que podem facilitar a vida de quem pretende escrever
um aplicativo de linha de comando, vou listar algumas:

* [python-fire](https://github.com/google/python-fire)
* [click](http://click.pocoo.org/)
* [docopt](https://github.com/docopt/docopt)

Você pode testá-las e concluir se alguma se encaixa melhor no seu problema ou se
a standard library do python já é o suficiente.

**Referências**<br>
[Argparse Official Documentation](https://docs.python.org/3/library/argparse.html)<br>
[Argparse tutorial](https://docs.python.org/3/howto/argparse.html)<br>
[Python Argparse Cookbook](https://mkaz.tech/python-argparse-cookbook.html)<br>
[argparse – Command line option and argument parsing](https://pymotw.com/2/argparse/)<br>
