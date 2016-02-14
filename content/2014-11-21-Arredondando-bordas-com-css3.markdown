Title: Arredondando bordas com CSS3
Date: 2014-11-21 00:00:00
Category: CSS
Tags: css, front-end, html

Uma das hypes atuais da web é o uso massivo de imagens redondas, principalmente em avatares. Google, Facebook, Instagram e iOS, são só alguns exemplos de grandes nomes do design que aderiram a essa tendencia. Mas calma, se você quer pegar carona nessa onda, você não precisa ficar editando imagem por imagem do seu site.

<!-- more -->
### Então "Comofas"?
Com o **CSS3**, conseguir esse efeito é _moleza_, basta utilizar a propriedades **border-radius**. Essa propriedade recebe como valor uma porcentagem ou uma medida em pixels, que determina quanto a borda do elemento deverá ser arredondada.

### De Quadrado para Circulo
Transformar uma imagem quadrada em uma imagem redonda é muito simples, basta determinar sua propriedade _border-radius_ com 50%.

```css
.avatar {
    border-radius: 50%;
}
```

Agora, qualquer elemento html (de preferencia quadrado) que seja da classe **avatar**, será transformado em um circulo.

```html
<img class="avatar" src="img/photo.jpg" />
```
Veja o resultado com uma imagem aleatória

<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/62yPB/9/embedded/result,html,css" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

### Arredondando cantos
Se a sua intenção não for criar circulos, você pode diminuir a porcentagem do raio (radius) ou trabalhar com pixels. Você pode também arredondar somente cantos específicos de um elemento. Assim como a grande maioria das propriedades do CSS, a propriedade _border-radius_ consiste em um conjunto de popriedades especificas para cada canto de um elemento, como por exemplo a propriedade **border-top-left-radius**.
Para arredondar somente os cantos inferiores de um elemento, podemos fazer da seguinte forma.

```css
.inferior {
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
}
```

ou assim

```css
.inferior {
    border-radius: 0 0 30px 30px;
}
```

Veja esse exemplo com a mesma imagem aleatória anterior

<iframe width="100%" height="300" src="http://jsfiddle.net/drgarcia1986/Jjy5K/4/embedded/result,html,css" allowfullscreen="allowfullscreen" frameborder="0"></iframe>

### É Cross-Browser?
Realizei testes tanto com o Firefox (gecko) como com Chrome (webkit) e não tive problemas, o IE 9 (trident) também já está compativel, mas por garantia e compatibilidade com versões antigas de outros browsers, você pode usar as propriedades especificas de cada motor de renderização

```css
.seletor {
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
}
```

#### Referências
[Cantos arredondados no IE 9](http://msdn.microsoft.com/pt-br/library/gg589503%28v=vs.85%29.aspx)<br />
[border-radius - CSS Tricks](http://css-tricks.com/almanac/properties/b/border-radius/)<br />
