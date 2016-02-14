Title: String Format no JavaScript
Date: 2014-11-20 00:00
Category: JavaScript
Tags: prototype, javascript

Nessa minha recente aproximação com o **JavaScript**, a primeira coisa que senti falta foi de um método do tipo _Format_ para trabalhar com strings.

<!-- more -->
### Decepção
Confesso que foi uma triste surpresa saber que nativamente o JavaScript não possui um método para essa finalidade. Nesse momento me imaginei fazendo esse tipo de concatenação:

```javascript
var texto = 'Olá ' + nome + ', seja bem vindo ao site ' + site + '\nVocê é realmente ' + nome + '?';
```

### Esperança
Da mesma forma que fui surpreendido negativamente, também tive uma ótima surpresa ao descobrir que o JavaScript permite _tunar_ seus objetos, incluido novas propriedades e novos métodos, graças a propriedade **prototype**. Com isso o céu é o limite.

### Solução
O seguinte código cria um método chamado **format** no prototype dos objetos **Strings**, tornando esse método disponível para qualquer string do código:

```javascript
if (!String.prototype.format) {
    String.prototype.format = function() {
        var formatted = this;
        for (var i = 0; i < arguments.length; i++) {
            var regexp = new RegExp('\\{'+i+'\\}', 'gi');
            formatted = formatted.replace(regexp, arguments[i]);
        }
        return formatted;
    }
};
```

Ao colocar esse código no ~~head do html na tag script~~ início do seu arquivo _JS_, você será capaz de montar o texto do primeiro exemplo da seguinte forma:

```javascript
var texto = 'Olá {0}, seja bem vindo ao site {1}\nVocê é realmente {0}?'.format(nome, site);

```

Com certeza mais elegante e mais aderente a outras linguagens, como por exemplo o Python.

### Explicação
Neste código mágico primeiro verificamos se a propriedade _format_ do prototype de String está nula, caso esteja, atribuimos a ela um método que basicamente recupera o valor do objeto com o **this** (no caso, o conteúdo da string) e executa um for em cada argumento passado para esse método, esse _for_ substitui todas as ocorrências de _{N}_, pelo valor do argumento em seu determinado índice. Por exemplo, o resultado deste código:

```javascript
'Seja bem vindo {1}, {0}.'.format('Diego', 'Garcia');

```
Será:

```
Seja bem vindo Garcia, Diego.
```

### Possibilidade
As possibilidades com o uso do prototype são infinitas, comparando a outras linguagens, o prototype nos permite criar **class helpers** em JavaScript, o que por si só, já é incrivel.

#### Referências
[Prototype String - W3Schools](http://www.w3schools.com/jsref/jsref_prototype_string.asp)<br />
[JavaScript equivalent to Printf -  StackOverFlow](http://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format)<br />
[Date Helper - CodeProject](http://www.codeproject.com/Tips/59262/JavaScript-date-helper-class)<br />

