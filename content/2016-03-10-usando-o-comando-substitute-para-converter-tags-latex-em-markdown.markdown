Title: Usando o comando :substitute para converter tags LaTeX para Markdown
Date: 2016-03-10 10:00
Category: Vim
Tags: regex, vim

Recentemente decidi que iria ajudar o brother [Cássio Botaro](http://cassiobotaro.github.io/) na nobre tarefa de migrar o clássico **vimbook**
para o [gitbook](https://www.gitbook.com/) (você também pode ajudar acessando o [repositório do projeto](https://github.com/cassiobotaro/vimbook)).
Porém a versão anterior foi feita utilizando `LaTeX`, enquanto que a nova, necessita ser feita em `markdown`.
Eu poderia simplesmente substituir manualmente todas as tags _LaTeX_ por tags markdown, mas, sou muito preguiçoso pra isso.

<!-- more -->

### O que foi preciso fazer
Escolhi um capítulo para converter e precisava além de converter, dividir os "títulos" (ou sessões) do capítulo em arquivos separados.
O texto no geral não tem diferenças, o que muda porém, são as tags de formatação de texto, como por exemplo, títulos, ênfase, links, etc.
Sendo assim, eu basicamente precisava copiar as sessões para novos arquivos e substituir as tags _LaTeX_ por tags _markdown_.

Substituir as tag _LaTeX_ de forma manual seria algo extremamente tedioso e me levaria horas e mais horas.
Mas como você deve imaginar, uso o `VIM` e como já disse, sou preguiçoso, então fui atrás de uma solução mais criativa.

### O Comando :substitute
O Vim possui o comando `:substitute` (abreviado como `:s`) que funciona como um _"procurar & substituir"_.
Ele funciona da seguinte maneira, procura por um padrão e caso encontre um texto que case com esse padrão, substitue por outro.
A syntax do comando _:substituite_ é a seguinte:
```vim
:[range]s[ubstitute]/{pattern}/{string}/[flags] [count]
```
Por exemplo, no texto:
```
Use Python2 e sua vida será melhor
```
Com o cursor na linha onde o texto se encontra, podemos aplicar o seguinte comando de substituição:
```vim
:s/Python2/Python3/
```
Obviamente o resultado será:
```
Use Python3 e sua vida será melhor
```
Simples não? Por padrão, se não especificarmos o `range` de atuação, o comando _:substitute_ só terá efeito na linha corrente,
porém, para realizar a busca em todo o arquivo basta utilizar o _range_ `%` (que significa `1,$`, ou seja, do início ao fim do arquivo corrente):
```vim
:%s/Python2/Python3/
```
Outro detalhe é que, da forma como está o comando, somente a primeira ocorrência do texto _Python2_ seria substituída.
Se a intenção for substituir todas as ocorrências do texto, é possível utilizar a _flag_ `g`:
```vim
:s/Python2/Python3/g
```
Para saber mais opções e formas de usar o comando _:substitute_, veja o _help_ através do comando `:help :substitute`.

### Utilizando Regex no comando :substitute
É possível utilizar _expressões regulares_ no comando _:substitute_ do Vim, o que significa que o céu é o limite.
Seguindo o exemplo anterior, poderíamos fazer a substituição utilizando uma regex:
```vim
:s/Python[1-2]\.\?[1-7]\?/Python3/
```
Dessa forma, substituiria não só o texto _Python2_, como também, _Python2.7_, _Python2.6_, _Python1_, etc.

#### O modificador _very magic_
Se você já está familiarizado com _expressões regulares_, deve ter notado o _escape_ incomum no quantificador `?`.
Isso ocorre pelo fato de que tantos os _meta-caracteres_, quanto os _quantificadores_ e os indicadores de _grupo_ precisam ser escapados no comando _:substitute_.
Porém, existe uma forma de evitar isso, usando o modificador `very magic` (`\v`).
Aplicando o modificador _very magic_ no comando anterior, ficaria desta forma:
```vim
:s/\vPython[1-2].?[1-7]?/Python3/
```
Como essa é uma _regex_ simples, não é possível notar um ganho muito grande, porém, imagine uma regex um pouco mais complexa:
```vim
:s/\d\{2,5\}\(\D\+\)\d\{1,3\}//
```
Ativando o modificador _very magic_ ficaria dessa forma:
```vim
:s/\v\d{2,5}(\D+)\d{1,3}//
```
Sendo assim, se você se perder nas barras de _escape_, já sabe o que fazer.

### Alguns truques de Regex que usei
Voltando ao desafio de migrar de _LaTeX_ para _markdown_, para usar comandos e regex genéricas, eu teria que usar alguns artifícios, como `grupos` e `retrovisores`.

#### Grupos
Grupos em regex são definidos por _parênteses_ e servem a vários propósitos.
No caso em que estamos discutindo, a idéia é, recuperar valores de dentro de uma _tag_.
Por exemplo, imagine o seguinte texto:
```xml
<name>Diego Garcia</name>
```
E imagine que a idéia seria recuperar apenas o conteúdo da tag `<name>` e separar entre primeiro e segundo nome (no caso _Diego_ e _Garcia_), sendo assim, poderiamos usar a seguinte regex:
```regex
<name>(\w+)\s(\w+)<\/name>
```
O resultado seria:
```yaml
Match: "<name>Diego Garcia</name>"
    Group 1: "Diego"
    Group 2: "Garcia"
```
Ou seja, a frase inteira teria dado _match_, porém, eu teria somente o texto _Diego_ no grupo 1 e o texto _Garcia_ no grupo 2 da minha regex.

#### Retrovisor
Quando utilizamos grupos em regex, podemos utilizar também _retrovisores_ para referenciarmos os valores recuperados nos grupos.
Os _retrovisores_ são representados por uma barra invertida e o número do grupo capturado, por exemplo `\1`.
Usando o mesmo exemplo anterior junto ao comando _:substitute_ do vim, podemos por exemplo, separar esse texto em duas tags:
```vim
s/<name>\(\w\+\)\s\(\w\+\)<\/name>/<first>\1<\/first><last>\2<\/last>/
```
o resultado do comando anterior seria:
```xml
<first>Diego</first><last>Garcia</last>
```

### Utilizando funções no comando :substitute
O Vim possui diversas funções builtin e elas podem ser usadas também no comando _:substitute_.
Por exemplo, vamos imaginar uma simples conta matemática:
```
10 + 3 = ?
```
Podemos realizar esse cálculo utilizando a função `eval`:
```vim
:echo eval("10 + 3")
```
> É possível também fazer simplesmente `:echo 10 + 3` mas usaremos o **eval** mais a frente

Porém, imagine um arquivo com várias dessas contas, com o comando _:substitute_ e a função _eval_ é possível realizar essas contas em massa.
Para isso, primeiro precisamos capturar a expressão com uma regex e usar a função `submatch` para recuperar esse valor capturado.
A função _submatch_ funciona como os retrovisores, retornando os grupos de captura.

```vim
:%s/^\([^=]*\)=\s*?/\=submatch(1) . '= ' . eval(submatch(1))/g
```
Note que estamos substituindo todo texto pela expressão matemática e seu resultado.
Para utilizar funções no comando _:substitute_ basta utilizar o caracter especial `=`.
Outro detalhe importate é o fato de que para concatenar strings em funções no Vim, utilizasse o ponto (`.`).

Para mais informações sobre as funções builtin do Vim, veja o _help_ com o comando `:h functions`.

### Substituições
Chega de explicações e teorias, vamos as substituições práticas que fiz entre tags _LaTeX_ e tags _markdown_.
Basicamente todas as substituições seguiram o mesmo padrão, um pattern que case com o texto,
um grupo (ou mais) envolvendo a informação que quero recuperar e o uso de retrovisores na forma como desejo substituir o texto.

#### Ênfase (ou itálico)
Em _LaTeX_ para dar ênfase a um texto, utilizamos o seguinte padrão:
```latex
{\em Texto}
```
Enquanto que, em markdown, podemos fazer desta forma:
```markdown
*Texto*
```
> Também é possível utilizar o **underscore**: `_Texto_`

Sendo assim, para fazer essa conversão, eu poderia usar o padrão `{\\em ([^}]*)}`, onde, após o texto **{em** e o espaço, crio um grupo de captura que pegue
qualquer texto diferente do caracter **}** (a lista negada `[^}]`) em zero ou qualquer quantidade (quantificador `*`) e para fechar, indico o caracter **}**
para que também possa ser substituido na execução do comando.
Convertendo essa regex para o comando _:substitute_ do Vim, já utilizando o retrovisor correspondente ao grupo de captura
para formatar o texto no padrão markdown (`*\1*`), teremos o seguinte comando:

```vim
:%s/{\\em \([^}]*\)}/*\1*/g
```
Para surtir efeito em todo arquivo, adicionei o _range_ `%` e para o comando ser aplicado a todas ocorrências que casarem com o padrão, utilizei a flag `g`.

#### Typewrite typeface
Seguindo a mesma lógica usada para converter texto em ênfase, também foram convertidos textos com _typewrite/typeface_, que usam a seguinte notação:

```latex
{\tt Texto}
```
A idéia era converter para texto em highlight, que no markdown, é feito da seguinte forma:
```markdown
`Texto`
```
Como disse, a lógica do comando de substituição nesse caso é basicamente a mesma usada para os textos com ênfase, só substituindo o _\em_ por _\tt_:
```vim
:%s/{\\tt \([^}]*\)}/`\1`/g
```
O resto do comando segue o mesmo mecanismo.

#### SubSection
_SubSection_ em _LaTeX_ são como _subtitulos_ de capítulos e usam a seguinte syntax:
```latex
\subsection{Texto}
```
No _vimbook_, as _subsections_ foram convertidas para o terceiro nível de cabeçalho (ou `H3` do _html_), que em markdown usa a seguinte syntax:
```markdown
### Texto
```
Sem muito segredo para fazer a substituição, a regex `\\subsection{([^}]*)}` já é o suficiente, pois básicamente estamos recuperando o conteúdo dentro
das chaves (`{}`) através de um grupo de captura que recupera tudo que for diferente do caracter de fechamento de chaves (`([^}]*)`).
Dessa forma, podemos usar esse conteúdo em um retrovisor e assim montar nosso subtítulo formatado em markdown (`### \1`).
```vim
:%s/\\subsection{\([^}]*\)}/### \1/g
```
> Devido ao uso massivo de `{}` nas regex, optei por não usar o modificador *very magic*

#### Link
Links em _LaTeX_ são ligeiramente parecidos com markdown, você define o link e um texto de exibição desse link, utilizando a seguinte notação:
```latex
\href{http://link.com}{texto}
```
Em markdown é um pouco mais simples e invertido, primeiro se é definido o texto para depois definir o link:
```markdown
[texto](http://link.com)
```
Para realizar essa conversão serão necessários dois grupos de captura, um para o _link_ e outro para o _texto_.
A regex `\\href{([^}]*)}{([^}]*)}` já da conta do recado.
Apesar de ser um pouco grande, não tem segredo, note que repeti o mesmo mecanismo das outras regex, grupos de captura que pegam tudo que não for o
caracter de fechamento do trecho de interesse (que em todos os casos, consiste no fechamento de chaves **}**).
```vim
:%s/\\href{\([^}]*\)}{\([^}]*\)}/[\2](\1)/g
```
No padrão da substituição, basta fazer referência aos retrovisores dos grupos capturados e formatar na notação de links markdown.

#### Section
Por fim, _section_ em _LaTeX_, são títulos de capítulos e são descritos utilizando a seguinte notação:
```latex
\section{Texto}
```
No _vimbook_ cada _section_ basicamente se torna um arquivo separado e o título da _section_ se torna o _header_ da página, utilizando
o segundo nível de cabeçalho (`H2` no _html_).
Outro detalhe do _vimbook_ é que os cabeçalhos principais (`H1` e `H2`) utilizam o estilo **setext** e os demais utilizam o padrão **atx**.

> Veja mais sobre o estilo **setext**, **atx** e markdown em geral [neste link](https://daringfireball.net/projects/markdown/syntax).

Sendo assim, as _sections_ foram convertidas utilizando o seguinte padrão markdown:

```markdown
Texto
-----
```
Para recuperar o conteúdo referente ao título da section, podemos usa a regex `\\section{([^}]*)}` que basicamente segue o mesmo padrão das outras que fizemos,
porém, nesse ponto temos um problema.
Como criar um comando genérico de substituição que coloque o caracter `-` _n vezes_,
de acordo com o tamanho do texto recuperado em um grupo de captura?
Simples, `functions`!

Utilizaremos 3 funções:

* **submatch**: semelhante ao retrovisor, retorna o valor de um grupo de captura.
* **repeat**: retorna a repetição de uma string _n_ vezes.
* **strlen**: retorna o tamanho de uma determinada string.

Então precisamos, imprimir o texto capturado no primeiro grupo de captura (`submatch(1)`), adicionar uma quebra de linha (`\r`) e repetir o caracter
`-` (`repeat('-', count)`) tantas vezes quanto o tamanho do texto capturado (`strlen(submatch(1))`).
No final, temos o seguinte comando:
```vim
:%s/\\section{\([^}]*\)}/\=submatch(1) . "\r" . repeat('-',strlen(submatch(1)))/g
```
Pronto, com esses comandos toda a mágica acontece e não é preciso fazer diversar alterações repetitivas de forma manual.

### Observação
Todos os recursos utilizados como _pattern_ nas pesquisas do comando _:substitute_, também são válidos paras as busca simples do Vim (comando `/`).

### Alternativas
Todo esse processo poderia ter sido feito também utilizando o `SED`, mas como outras edições foram necessárias, optei por fazer no Vim.

**Referências**<br>
[Vimbook](https://www.gitbook.com/book/cassiobotaro/vimbook/details)<br>
[:help :substitute](http://vimdoc.sourceforge.net/htmldoc/change.html#:substitute)<br>
[Search and Replace](http://vim.wikia.com/wiki/Search_and_replace)<br>
[:help functions](http://vimdoc.sourceforge.net/htmldoc/eval.html#functions)<br>
[Expressões Regulares - Guia de Consulta Rápida](http://aurelio.net/regex/guia/)
