Title: Validações de formulários e inputs
Date: 2014-11-23 10:13:03
Category: HTML
Tags: html, forms, javascript

Qualquer um sabe que é praticamente impossível encontrar sites sem nenhum formulário, nem que seja apenas para contato com o autor. O que algumas pessoas não sabem é que o **HTML5** adicionou algumas novas facilidades para lidarmos com formulários e inputs, algumas até, podem aposentar os antigos códigos de válidação em _JavaScript_.

<!-- more -->
### RegEx
Para demonstrar validações com RegEx em formulários e inputs, já iremos começar com o caso mais comum, **e-mail**. Seja para um formulário de fale-conosco, comentários em um blogs, cadastros, etc, e-mail costuma ser o dado mais comum na internet.

#### Ao modo JavaScript
O modo mais comum de fazer qualquer validação em formulários HTML é com certeza o JavaScript. Para nosso exemplo iremos criar uma função chamada _validarEmail()_ que irá receber como parametro o endereço de e-mail que deverá ser validado e o _id_ de uma _div_ de mensagem genérica. Essa função fará a validação com **RegEx** e irá mostrar uma mensagem na div indicando o resultado da validação.

```javascript
function validarEmail(email, validacao) {
    var ck_email = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    var valid = document.getElementById(validacao);
    result = ck_email.test(email);
    if (!result) {
        valid.innerHTML = "Endereço de e-mail inválido";
    } else {
        valid.innerHTML = "Endereço de e-mail válido";
    }
    return result;
}
```

Nesse exemplo, faremos essa validação no evento **onBlur** do input, ou seja, quando o input perder o foco.

``` HTML
<p>Digite seu e-mail:
    <input name="email" id="email" onBlur="validarEmail(this.value, 'validacao');" />
</p>
<div id="validacao"></div>
```
Veja o resultado

<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/3H2EU/2/embedded/result,js,html" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

#### Ao modo HTML5
Com o **HTML5** agora podemos realizar validações baseadas em _RegEx_ direto no input, através da propriedade **pattern**.

``` HTML
<input name="email" pattern="^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$" id="email" type="text" />
```
A principal diferença desta abordagem é o momento da validação. A validação baseada no pattern (assim como outras validações próprias do html5) estão diretamente ligadas a formulários, ou seja, a validação será executada somente no momento do _submit_ do formulário.

Para não estender muito o post, as próximas validações faremos somente ao modo **HTML5**.

### Campo obrigatório
A validação de campo obrigatório é moleza somente com recursos do HTML5, basta adicionar no input a propriedade **required** e toda a mágica é feita :) .

``` HTML
<input name="nome" id="nome" type="text" required />
```

### Tipo do campo
Uma forma muito útil e simples de validar e estilizar o conteúdo de um input é determinando o seu tipo (_type_). Por exemplo, para um campo que deverá armazenar números, podemos usar um input do tipo **number**. Inclusive, com o tipo number é possível determinar um numero mínimo e um número máximo que o input deve aceitar, através das propriedades **min** e **max**.

``` HTML
<input name="qtde" id="qtde" type="number" min="3" max="10"/>
```

Existe um série de outros tipos específicos de inputs que podem nos fazer poupar muito trabalho, veja uma pequena lista:

* number
* range
* url
* e-mail (sim, existe, porém a validação não é tão poderosa)
* entre outros.

Veja exemplos dos tipos acima
<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/uqkxd2v3/embedded/result,html" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

Esses tipos específicos são muito úteis para sites voltados para mobile, pois os navegadores mobile já estão preparados para exibir ao usuário somente a opção de teclado compatível com o input.

### Estilizando inputs de acordo com a validação
É possível de forma simples e genérica aplicar estilos CSS em inputs com valores válidos ou inválidos, de acordo com as regras que você determinar. Por exemplo, criaremos um padrão em que inputs inválidos terão o fundo avermelhando e os inputs válidos terão o fundo azulado.

```css
input:invalid, input:focus:invalid {
    background-color: #F08080;
}
input:valid {
    background-color: #87CEFA;
}
```

Para testarmos esse estilo, usaremos dois inputs, um do tipo _text_ porém de preenchimento obrigatório (_required_) e um do tipo _number_ com o valor mínimo de 18.

``` HTML
Nome: <input id="nome" name="nome" type="text" required /><br />
Idade: <input id="idade" name="idade" type="number" min="18" /><br />
```

Simples, prático e o melhor de tudo, genérico. Veja esse código funcionando:
<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/wtku5m7L/1/embedded/result,html,css" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

Para deixar a aparência ainda mais profissional, podemos utilizar imagens nos inputs. Faremos o mesmo exemplo, porém, ao invés de usarmos cores de fundo nos inputs, iremos acrescentar pequenos icones após o conteúdo, indicado se o campo está válido ou inválido.

```css
input:invalid, input:focus:invalid {
     background-image: url(/imgs/invalid.png);
     background-position: right top;
     background-repeat: no-repeat;
 }
 input:valid {
     background-image: url(/imgs/valid.png);
     background-position: right top;
     background-repeat: no-repeat;
 }
```
O efeito no input do tipo number não é muito agradável, demonstrarei somente no campo do tipo text.
<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/wnjLjfcy/1/embedded/result,html,css" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

Outra forma excelente de obter um efeito semelhante a este é utilizando os pseudo-elementos **after** ou **before**. Faremos uma pequena alteração no HTML, adicionando um _label_ para cada input.

``` HTML
<input id="nome" name="nome" type="text" required />
<label for="nome">Nome</label>
<input id="idade" name="idade" type="number" min="18" />
<label for="idade">Idade</label>
```

Após o conteúdo deste label, iremos adicionar o simbolo **X** para os inputs inválidos e o simbolo **✓** para os inputs válidos, utilizando o pseudo-elemento _after_.

```css
input:invalid + label::after {
    content:' X';
}
input:valid + label::after {
    content:' ✓';
}
```

Veja o resultado:
<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/gzn6muzu/1/embedded/result,html,css" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

### Customizando as mensagens de validação padrão
Para finalizar, se você já testou fazer validações com o _pattern_ dos inputs, já deve ter notado que a mensagem que é exibida indicando que o conteúdo do input está inválido é muito genérica, no Firefox por exemplo a mensagem exibida é _"Por favor, satisfaça o formato requisitado"_.
Existe uma forma de modificar essa mensagem via javascript, através do método **setCustomValidity** aplicado no evento **oninvalid** do input. Por exemplo, vamos imaginar um input que irá receber uma senha e essa senha pode conter qualquer tipo de caracter, porém, deverá ter um tamanho minímo de 8 caracteres.

``` HTML
<input name="senha" oninvalid="this.setCustomValidity('No m&iacute;nimo 8 caracteres')" oninput="this.setCustomValidity('')" type="password" id="senha" pattern=".{8,}" required />
```

Note que foi necessário manipular o _CustomValidity_ setando uma string vazia no evento **oninput** do input, isso porque, ao setar o CustomValidity com algum valor, o html interpreta que o input está inválido e não muda esse estado mesmo alterando o conteúdo para algo válido.
<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/4wfmphhj/embedded/result,html" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

#### Referências
[Input Pattern - W3Schools](http://www.w3schools.com/tags/att_input_pattern.asp) <br />
[Html5 form validation - Art of Web](http://www.the-art-of-web.com/html/html5-form-validation/) <br />
[Set Custom Validation Message - Stackoverflow](http://stackoverflow.com/questions/5272433/html5-form-required-attribute-set-custom-validation-message) <br />
[CSS Pseudo Elements](http://www.w3schools.com/css/css_pseudo_elements.asp)
