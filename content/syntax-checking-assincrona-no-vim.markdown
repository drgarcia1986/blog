Title: Syntax Checking Assíncrona no VIM
Date: 2016-07-05 10:00
Category: Vim
Tags: vim, python

Syntax Checking é algo básico e corriqueiro na vida de um desenvolvedor.
O ideal é que sempre que alguma alteração seja feita no código, algum syntax checking 
verifique esse código a fim de evitar erros mais básicos e manter uma boa formatação e consistência.
Se você é usuário do **vim** (assim como eu), muito provavelmente utiliza o plugin
[syntastic](https://github.com/scrooloose/syntastic) para esse fim.
Porém, tenho certeza que ao menos uma vez, você já se incomodou com a lentidão na execução desse plugin.
Eu já e é por isso que procurei uma alternativa.

<!-- more -->

## Por que é lento?
(comentar que é executado no BufWrite e que é sincrono)

## Compiler e o comando :make
(Explicar o compiler, make e quickfix do vim)

## Vim-dispatch
(falar sobre o plugin e explicar a execução assíncrona)

## Python-compilers
(falar do meu projeto e dos compilers disponíveis)
(mostrar um exemplo de como usar os dois em conjunto)
(mostrar um print da parada funfando seria legal)


## Vim8 e NeoVim
(explicar que os dois trabalham com esquema async)

**Referências**<br>
[:help quickfix](http://vimdoc.sourceforge.net/htmldoc/quickfix.html)
