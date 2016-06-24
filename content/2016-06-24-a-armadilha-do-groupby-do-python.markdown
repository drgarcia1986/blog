Title: A armadilha do groupby do Python
Date: 2016-06-24 10:00
Category: Python
Tags: python, itertools

O `itertools` é um módulo fantástico da bibliotéca padrão do python, para trabalhar com iteradores e estruturas complexas de dados.
Porém, é recomendado um conhecimento mínimo sobre geradores para evitar possíveis armadilhas.
Sim, eu cai em mais uma [armadilha](/2015/06/07/a-armadilha-dos-argumentos-com-valores-default/) do Python, dessa vez foi o `groupby` do
módulo _itertools_.

<!-- more -->

### O que é o `groupby` ?
O _groupby_ consiste em uma função que, baseado em um iterável, retorna uma estrutura de agrupamendo com um valor de chave e um grupo de valores,
relacionados a essa chave.
A função _groupby_ possui a seguinte syntax:

```python
def groupby(iterable, key=None)
```

Onde:

* **Iterable**: Qualquer iterável (e.g. _lista_, _tupla_, _gerador_, _dicionário_, etc.).
* **key**: Uma _key function_ que será aplicada em cada elemento do iterável afim de retornar a chave para o agrupamento.

O resultado da função _groupby_ é um gerador onde cada iteração retorna o valor da _chave_ e outro gerador com os valores
que foram agrupados para essa chave, por exemplo:
```python
>>> from itertools import groupby
>>> items = [('animal', 'dog'), ('animal', 'cat'), ('person', 'john')]
>>> for thing, values in groupby(items, key=lambda x: x[0]):
...     print('{}: {}'.format(thing, list(values)))
...
animal: [('animal', 'dog'), ('animal', 'cat')]
person: [('person', 'john')]
```

> Usei o `list()` no `values` para poder resolver o gerador e apresentar os valores no print (não a instancia do gerador).

### A armadilha
Como você pode ver, o _groupby_ é realmente muito útil e poderoso, porém, o que poderia acontecer caso o iterável não estivesse
préviamente ordenado pelo mesmo critério a ser utilizado para o agrupamento?
Vamos adaptar o exemplo anterior para realizar esse teste:

```python
>>> from itertools import groupby
>>> items = [('animal', 'dog'), ('person', 'john'), ('animal', 'cat')]
>>> for thing, values in groupby(items, key=lambda x: x[0]):
...     print('{}: {}'.format(thing, list(values)))
...
animal: [('animal', 'dog')]
person: [('person', 'john')]
animal: [('animal', 'cat')]
```
Como você pode ver, o agrupamento falha, retornado a mesma chave mais de uma vez com um grupo de valores distintos.

### Por que isso acontece ?
Isso acontece porque internamente, o _groupby_ gera um novo grupo a cada novo valor de chave que for encontrado no iterável.
Mesmo que uma chave se repita, o _groupby_ não consegue "olhar para atrás" e verificar os grupos que já foram gerados.

### Como resolver?
Simples, basta antes de agrupar, ordenar o iterável pela mesma chave que será utlizada no agrupamento do _groupby_, por exemplo:

```python
>>> from itertools import groupby
>>> items = [('animal', 'dog'), ('person', 'john'), ('animal', 'cat')]
>>> ordered_items = sorted(items, key=lambda x: x[0])
>>> for thing, values in groupby(ordered_items, key=lambda x: x[0]):
...     print('{}: {}'.format(thing, list(values)))
...
animal: [('animal', 'dog'), ('animal', 'cat')]
person: [('person', 'john')]
```

### Como se prevenir?
Simples, **leia a documentação**!!!
Sim, meu vacilo foi ainda maior pois, a documentação oficial do python alerta sobre esse risco:

> The operation of groupby() is similar to the uniq filter in Unix. It generates a break or new group every time the value of the key function changes (which is why it is usually necessary to have sorted the data using the same key function). That behavior differs from SQL’s GROUP BY which aggregates common elements regardless of their input order.

Tudo bem que poderia ter um destaque maior esse alerta ou até mesmo um exemplo, porém, não adianta reclamar que não está documentado =).

**Referências**<br>
[Documentação Oficial](https://docs.python.org/3.4/library/itertools.html#itertools.groupby)
