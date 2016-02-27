Title: MultiProcess em Python e o drible no GIL
Date: 2016-02-27 14:00
Category: Python
Tags: python, process

Se você leu o post anterior sobre [threads em python](/2016/02/18/threads-em-python-e-claro/), muito provavelmente percebeu que o fato do `CPython` ser otimizado para executar códigos _singlethread_, não é um impeditivo para execução de tarefas paralelas com alto desempenho.
Porém, threads resolvem com maestria a execução de tarefas de **I/O Bound** paralelas, mas quando o assunto é **CPU Bound**, existe uma outra forma de ser efetivo no paralelismo com python.

<!-- more -->

### Ainda o GIL
Assim como na execução singlethread, o `GIL` **NÃO** é liberado para tarefas do tipo _CPU Bound_ (ou seja, que dependem do uso massivo do processador e não de _I/O_).
Mesmo que sejam criadas inúmeras threads para execução desse tipo de tarefa, o desempenho final não seria satisfatório, pelo contrário, o desempenho singlethread seria melhor do que o multithread.

Porém, existe outra forma de lidar com esse problema, _processos_.
Veja como isso funciona.

### Encontrando os números primos
Para demonstrar o uso de multi processamento no python partiremos para um exemplo totalmente didático.
Faremos uma função que retorna uma lista com o números primos até um determinado número limite.

```python
def primes_until(num):
    result = []
    for p in range(2, num+1):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            result.append(p)
    return result
```

Por exemplo, ao executar a função `primes_until` passando o número `10` como argumento, teremos o seguinte retorno:

```python
>>> primes_until(10)
[2, 3, 5, 7]
```
> Números primos são os números naturais que têm apenas dois divisores diferentes: o 1 e ele mesmo. [fonte](http://www.somatematica.com.br/fundam/primos.php)

Como essa função não exige muito poder computacional para ser executada, daremos uma _forçada na barra_ para que a execução fique lenta o suficiente a ponto de compensar o multi processamento.
Executaremos a função `primes_until` _14_ vezes passando como número limite o range de _1000_ até _15000_ saltando de _1000_ em _1000_.

```python
TO_CALCULATE = range(1000, 15000, 1000)
```

### Execução Serial
Para realizar esses cálculos de forma serial, iremos iterar sobre o gerador `TO_CALCULATE` que especificamos anteriormente e para cada número gerado iremos executar a função `primes_until`.

```python
def run_serial():
    print({i: primes_until(i) for i in TO_CALCULATE})
```
> Como escrevo esses exemplos baseados no Python 3 a função built-in `range` se tornou um gerador. Para utiliza-la como gerador no Python 2 utilize a função `xrange`


### Execução multiprocess
Faremos o mesmo para realizar a execução multiprocess, porém, iremos distribuir cada execução em um processo diferente.
Assim como no post sobre [threads em python](/2016/02/18/threads-em-python-e-claro/), usaremos o módulo `concurrent.futures`, com a diferença que desta vez utilizaremos o `ProcessPoolExecutor` como nosso _executor_.
Criaremos `Futures` para cada execução (através do método `executor.submit()`) e depois através do gerador `as_completed()` iteraremos sobre as _futures_ (no caso nossos processos) que já estejam concluídas.

```python
from concurrent.futures import as_completed, ProcessPoolExecutor


def run_multiprocess():
    waits = {}
    with ProcessPoolExecutor() as executor:
        waits = {
            executor.submit(primes_until, i): i
            for i in TO_CALCULATE
        }
        print({
            waits[future]: future.result()
            for future in as_completed(waits)
        })
```
> Caso não seja especificado o parâmetro `max_workers` na criação da instancia do _ProcessPoolExecutor_, por padrão o python assume como sendo o número de processadores da máquina.

Ao realizar o `submit` da função *primes_until* para o nosso *ProcessPoolExecutor*, um fork do processo principal é criado e a execução é feita nesse processo separado de forma paralela.
Dessa forma, conseguimos dividir a execução em processo separados (com o **GIL** independente para cada um) e com isso não temos o efeito do _lock_ do GIL para cada requisição ao processador.

```bash
$ ps aux | grep python3
diego-g+ 10074  6.0  0.2 194720 12404 pts/24   Sl+  13:01   0:00 python3 primes_numbers.py multiprocess
diego-g+ 10075  121  0.1  47256  7936 pts/24   R+   13:01   0:01 python3 primes_numbers.py multiprocess
diego-g+ 10076  121  0.1  47256  7932 pts/24   R+   13:01   0:01 python3 primes_numbers.py multiprocess
diego-g+ 10077  119  0.1  47256  7940 pts/24   R+   13:01   0:01 python3 primes_numbers.py multiprocess
diego-g+ 10078  121  0.1  47256  7936 pts/24   R+   13:01   0:01 python3 primes_numbers.py multiprocess
```

### Comparando a execução
Como disse no começo desse post, a função *primes_until* não requer um grande poder de processamento para ser executada, mas como esse post tem fins didáticos, forçamos um conjudo de execuções pesadas a ponto de ficar muito demorado a excução singlethread.
Obviamente a execução multiprocess executa todos os calculos de uma só vez de forma paralela e sem intervenção do GIL (por se tratar de processos separados), com isso, conseguimos alcançar uma maior velocidade na execução.

* Execução serial
```
$ time python primes_numbers.py

real	0m6.366s
user	0m6.285s
sys	    0m0.076s
```

* Execução multiprocess
```
$ time python primes_numbers.py multiprocess

real	0m3.588s
user	0m12.186s
sys	    0m0.055s
```
> Se trocassamos o executor de _ProcessPoolExecutor_ para _ThreadPoolExecutor_ teriamos sérios problemas de performance, devido ao bloqueio do GIL a ponto de a execução singlethread ter um desempenho melhor.

Veja o código completo desse exemplo [neste gist](https://gist.github.com/drgarcia1986/b70c895b4d9b825f367f).

### O custo do uso de multi processamento
Apesar da execução multiprocess do exemplo anterior ter sido concluída em praticamente metade do tempo quando comparada a execução serial, não podemos encarar o multiprocess como a solução de todos os problemas em python.
Multiprocess não é uma bala de prata, muito pelo contrário, o seu uso deve ser muito ponderado.

O multiprocess tem um custo no python que muitas vezes não paga o seu uso, como por exemplo, o tempo de `fork` do processo, `serialização`(via pickle) dos dados, `comunicação` entre processos, etc.
A minha sugestão é, teste e compare antes de tomar uma decisão, se uma arquitetura multiprocess não for muito superior em termos de desempenho para o seu problema, não vale a pena manter essa complexidade.


### Alternativas
Antes de pensar em uma solução baseada em paralelismo, você pode executar o seu código em outros interpretadores do python como por exemplo o [pypy](http://pypy.org/) que promete ser um interpretador extremamente rápido e otimizado ou o [Cython](http://cython.org/) que tem uma relação mais amigavel com o **GIL**.


**Referências**<br>
[Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html)<br>
