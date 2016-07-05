Title: Threads em Python? é claro!
Date: 2016-02-18 10:00
Category: Python
Tags: python, threads

Muito provavelmente você já deve ter ouvido a mesma lenda que me foi contada quando estava apreendendo python:

_Python não é bom com threads_

Isso não é totalmente mentira, mas a questão é, threads só não serão efetivas com o python, se você não usar da forma correta.

<!-- more -->

### O temível GIL
O `CPython` (interpretador padrão do python) possui o **G**lobal **I**nterpreter **L**ock, também conhecido como `GIL`.
Um mecanismo (presente também em outras linguagens como o _Ruby_) responsável por prevenir o uso de paralelismo, fazendo com que apenas uma thread seja executada no interpretador por vez.
Isso faz com que, mesmo criando inúmeras threads, o desempenho de uma rotina singlethread será melhor do que o desempenho de uma rotina multithread, já que internamente, apenas uma thread estará fazendo uso da cpu por vez (mesmo em um ambiente multicore).

Existem vários beneficios e malefícios relacionados ao _GIL_ e talvez esse seja o motivo pelo qual muitas pessoas acreditam que em python, threads não são efetivas.

Porém, o que nem todos sabem é que para operações de `I/O` (network/socket e escrita em arquivos) o _GIL_ é liberado, ou seja, sempre que uma tarefa de _I/O_ for executada (por exemplo, consultar um servidor externo) o _GIL_ é liberado para que outro processo seja executado de forma paralela até essa primeira chamada retornar resultado.
Vamos ver isso na prática.

### Problema do mundo real: multiplos requests http
Uma situação muito comum no dia a dia de um desenvolvedor é ter que lidar com multiplos requests externos na mesma rotina.
Usaremos um exemplo ficticio de uma aplicação de linha de comando que imprimi a cotação do real em relação a algumas moedas estrangeiras.
Essas cotações serão recuperadas do site [Dolar Hoje](http://dolarhoje.com/) e sites similares.

### Recuperando as cotações
Recuperaremos as cotações das seguintes modeas: `dolar`, `euro`, `libra` e `peso`

```python
CURRENCY = {
    'dolar': 'http://dolarhoje.com/',
    'euro': 'http://eurohoje.com/',
    'libra': 'http://librahoje.com/',
    'peso': 'http://pesohoje.com/'
}
```

Como esses sites utilizam o mesmo formato, utilizaremos uma regex padrão para processa-los:

```python
DEFAULT_REGEX = r'<input type="text" id="nacional" value="([^"]+)"/>'
```

Para recuperar essas cotações, faremos uma espécie de web crawler que fara um `GET` na página e via `RegEx` será recuperada a informação sobre a cotação monetária.
O método para realizar esse request é extremamente simples:

```python
import re
from urllib.request import urlopen


def exchange_rate(url):
    response = urlopen(url).read().decode('utf-8')
    result = re.search(DEFAULT_REGEX, response)
    if result:
        return result.group(1)
```

Um simples `get` e `decode` do conteúdo de uma url através da `urlib` e a busca do padrão de uma regex através da função `search` do pacote `re` nativo do python para lidar com regex. <br>

> Utilizei a `urllib` por ser uma biblioteca nativa do python, porém, para esse tipo de operação (e qualquer outro tipo de request sincrono) recomendo o uso da bibliotéca [requests](http://docs.python-requests.org/en/master/)

### Execução serial
Para recuperar a cotação de todas as urls listadas no dicionáro `CURRENCY` de forma serial, basta iterar pelos `items` (chave, valor) desse dicionário, executando a função `exchange_rate` para cada um passando a url como parâmetro.

```python
for currency, url in CURRENCY.items():
    print('{}: R${}'.format(currency, exchange_rate(url)))
```

Cada iteração desse _for_ só será finalizada após a função `exchange_rate` processar a url informada, ou seja, o tempo demorado será algo em torno do tempo do primeiro request vezes o número de items do dicionário.

### Execução multithread
Para executar essa mesma rotina mas de forma paralela, utilizaremos a forma mais moderna de se trabalhar com concorrencia em python, o módulo `concurrent.futures`.
Esse módulo permite através de um `Executor` executar tarefas assincronas através de _threads_ ou _sub processos_.

> O módulo _concurrent.futures_ está disponivel apartir da versão 3.2 do python, porém, possui o backport [futures](https://pypi.python.org/pypi/futures) compatível com python 2.7

O módulo _concurrent.futures_ possuí 2 principais componentes:

* `Executor`: Interface que possui métodos para executar rotinas de forma assincrona.
* `Future`: Interface que encapsula a execução assincrona de uma rotina.

Para executarmos nossa função `exchange_rate` de forma assincrona deveremos executar o método `submit` do _executor_ (em nosso caso, uma instância de `ThreadPoolExecutor`).
Esse método aceita como parâmetro a função que será executada de forma assincrona e seus `*args` e `**kwargs`, no nosso caso devemos passar a função _exchange_rate_ e a _url_.
O método _submit_ retorna uma instância de _Future_ que encapsulara a execução assincrona da rotina.

Em nosso problema, precisamos iniciar todos os requests e aguardar até que todos sejam concluídos, para que isso seja possível basta criar _futures_ dessas rotinas e processar as que forem concluídas.

```python
from concurrent.futures import as_completed, ThreadPoolExecutor


with ThreadPoolExecutor(max_workers=len(CURRENCY)) as executor:
    waits = {
        executor.submit(exchange_rate, url): currency
        for currency, url in CURRENCY.items()
    }
    for future in as_completed(waits):
        currency = waits[future]
        print('{}: R${}'.format(currency, future.result()))
```
O gerador `as_completed` do módulo _concurrent.futures_ retorna as _futures_ que forem concluídas na ordem em que forem concluídas.
Após a _future_ estar concluída, basta recuperar seu resultado através do método `result()`.

> Repare que na criação do **executor** foi necessário especificar o número de workers que serão utilizados para executar as rotinas assincronas, porém, na versão 3.5 do python esse parâmetro não é mais obrigatório e caso ele seja omitido, o python assume o número de processadores na máquina

### Comparando a execução
Apesar de o mesmo numero de requests externos estarem sendo executados em ambos os casos, a execução serial executa um request por vez, enquanto que a execução multithread executa todos os requests de uma só vez, de forma paralela (sem intervenção do _GIL_) diminuindo assim o tempo de execução da aplicação de forma exponencial

* Execução serial
```
$ time python multi_requests.py
libra: R$5,78
dolar: R$4,00
euro: R$4,47
peso: R$0,27

real	0m3.476s
user	0m0.129s
sys	    0m0.004s
```
* Execução multithread
```
$ time python multi_requests.py threads
dolar: R$4,00
euro: R$4,47
libra: R$5,78
peso: R$0,27

real	0m1.433s
user	0m0.122s
sys	    0m0.025s
```
Note que a execução serial demorou em torno de **3.47 segundos** contra **1.43 segundos** da excução multithread.
Essa diferença tende a crescer de acordo com a quantidade de requests feitos.

Veja o código completo desse exemplo [neste gist](https://gist.github.com/drgarcia1986/2a5d283b0d279ea96c26).

### Conclusão

Em resumo, toda vez que alguém enche a boca para me dizer _"python não é bom com threads"_ essa é a minha reação:

(╯°□°）╯︵ ┻━┻

**Referências**<br>
[Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html)<br>
[Understanding the Python GIL](http://www.dabeaz.com/python/UnderstandingGIL.pdf)<br>
