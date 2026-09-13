---
title: 'Back to basics: Typescript'
description: 'Um pouco de nostalgia e vontade de ensinar algo novo, vou lançar a pill sobre Typescript.'
pubDate: 'Jun 22 2026'
tags: ['dev', 'tutorial']
hidden: false
---

# Pronto para uma viagem?

> Typescript é o Javascript do futuro sendo feito no passado e compilado no presente - Sun Tzu, provavelmente.

Agora que topou participar do bonde, deve tá se perguntando o que é o Typescript, correto? Fica tranquilo que Eu te respondo. E ainda mostro em exemplo, tudo isso fruto da minha vontade de voltar a ensinar.

```javascript
//javascript
function sum(a, b) {
  return a + b;
}

var n1 = 5;
var n2 = '5';
sum(n1, n2);
```

```typescript
// typescript
function sum(a: number, b: number): number {
  return a + b;
}

let n1 = 5;
let n2 = '5';
sum(n1, n2);
```

No nosso exemplo numero 1, que é um codigo simples que recebe dois valores em uma função e retorna a soma destes dois valores, mas como sabemos, o javascript não tem um freio de mão ou uma forma de evitar que você dê um tiro no pé em alguns momentos.

Neste caso, ele vai executar o código e retornar o valor `55`. Vai lá, eu espero você retornar do console do navegador.

Porque isso acontece? O JavaScript não faz verificação de tipos estática, os tipos só são avaliados em tempo de execução. quando chega a hora de validar, a informação já foi inserida e está em momento de execução, causando estas situações estranhas. No caso do nosso exemplo, ele cai para um `fallback` onde ao invés de retornar um erro, ele aplica uma coerção de tipos e `concatena` a informação ao invés de somar.

Tá Matheus, mas ai não poderiamos fazer isso aqui?

```javascript
//javascript
function sum(a, b) {
  return a + b;
}

var n1 = 5;
var n2 = '5';
sum(n1, Number(n2));
```

Sim, poderiamos. E isso serve muito bem pra scripts pequenos ou coisas que conseguimos aferir uma previsibilidade constante, não escala muito bem.

E é exatamente aí que o nosso tema de hoje entra em ação!

O Typescript surge com a proposta de ser uma linguagem compilada e com tipagem segura. Isso significa que nós escrevemos o código, aferimos tipos e quando terminamos o que estamos escrevendo, compilamos, e aí o compilador vai nos dizer se tem alguma coisa que não está cheirando bem no código, previnindo que casos assim acabem indo pra sua aplicação em produção.

No nosso caso do exemplo, quando rodarmos o nosso código, seja por meio do `tsc`, que é o Typescript compiler ou por meio do `Bun` que é um runtime de typescript similar ao `Node` ou `Deno`.

```typescript
// typescript
function sum(a: number, b: number): number {
  return a + b;
}

let n1 = 5;
let n2 = '5';
sum(n1, n2); // vai aparecer um erro do tipo "Argument of type 'string' is not assignable to parameter of type 'number'."
```

Vai em frente, acessa o https://www.typescriptlang.org/play e experimenta.

## Seguindo a toca do coelho

Agora que a primeira dose foi dada completamente de graça, vou te mostrar como pode começar a aplicar os conceitos de maneira homeopatica no teu projeto.

Bora construir juntinhos uma idéia e ver como que ela vai tomando vida.

Minha proposta é construirmos um pequeno programa que simula um mago, no qual a gente vai aprender sobre interfaces, classes, tipos, arrays e algumas coisitas mais. Vou tentar ser bem dinamico e didatico no processo.

Nosso objetivo final é uma aplicação em linha de comando (vulgo console) que vai simular um mago lançando bola de fogo, procurando conhecimento e depois listando todas as magias que adquiriu pelo conhecimento :)

### Primeiros passos

> Importante: Vou considerar que você vai usar o https://www.typescriptlang.org/play, não vou abordar sobre os ambientes e em como configurar o seu próprio nesse momento.

Vamos pensar o seguinte, como podemos modelar o nosso mago? Temos algumas opções, vou abordar a mais simples por aqui, as outras você pode pensar e tentar exercitar como dever de casa, também vou tentar fazer o mais acessivel possivel para qualquer um poder começar a programar.

O básico:

- definir o que é uma magia (interface)
- criar o mago (classe)
- dar ações ao mago (métodos)

E como nem tudo na vida é flor, alguns trechos vão ter pequenos bugs que você vai ter o prazer de corrigir para o nosso mago funcionar. Inclusive, precisamos de um nome para o nosso mago, certo? Vamos chamar ele de `Elminster`.

### Mão na massa

Para o Elminster ficar de boa em Faerun, ele precisa de algumas magias em seu grimório. Justamente nossa deixa para começar falando sobre `Union Types`.

Union type é um conjunto de tipos customizado que podemos criar, pensa nele como se fosse uma tipagem semelhante ao `int`, `string` ou `bool` porém com valores customizados por nós.

Através da declaração `type` nós criamos o tipo customizado chamado `Elemento` e utilizamos o sinal de igualdade para falar qual (ou quais) valores são permitidos. Caso seja necessário mais de um tipo, usamos o operador `|`, vulgo `OU (OR)` para atribuir mais valores.

Neste caso, podemos ler da seguinte maneira: O type Elemento pode receber os valores Fogo, Gelo OU Raio.

Caso a gente tente incluir um valor fora dos permitidos, vamos ter um erro de tipagem. Tenta atribuir um elemento `Agua` e vê o que acontece, depois volta aqui e adiciona o elemento agua no nosso union type :)

```typescript
type Elemento = 'fogo' | 'gelo' | 'raio';

const meuElemento: Elemento = 'fogo';
```

Agora que já tá um pouco mais habituado, bora seguir em frente.

O próximo passo é `interfaces`. Interfaces são como "contratos" na nossa aplicação, elas definem como as coisas devem se parecer e o que elas tem que receber.

Vamos pensar em um contrato de magia. Nós sabemos que a magia precisa de um nome, correto? Também sabemos que ela precisa de um elemento, assim como um valor de dano ou poder.

Que tal falarmos o seguinte: Minha interface é chamada Magia, ela possui um nome, um elemento e um dano? Da maneira Typescriptiana, isso é feito da seguinte maneira:

```typescript
interface Magia {
  nome: string;
  elemento: Elemento;
  dano: number;
}
```

Mamãozinho, né? Agora segura aí, vamos bolar a nossa primeira magia utilizando o nosso contrato.

Para isso, a gente precisa criar uma variavel, nesse caso vou usar `const` pois não planejamos alterar nossa magia depois de estudarmos ela.

Notou algo em comum com nossos exercicios anteriores?

```typescript
const bolaDeFogo: Magia = {
  nome: 'Bola de Fogo',
  elemento: 'fogo',
  dano: 30,
};
```

O atributo `elemento` da interface recebe o tipo Elemento do nosso `union type`, só vai aceitar os tipos legais que atribuimos no inicio do exercicio, qualquer outra coisa fora do escopo vai gerar um erro. Massa demais né?

Como exercicio, tenta fazer uma magia `Dardo de Choque` utilizando o Elemento `raio`.

```typescript
const dardoDeChoque: Magia = {
  nome: 'Dardo de Choque',
  elemento: 'raio',
  dano: 15,
};
```

Muito bom!! Já estamos na metade do processo, você tá arrasando no caminho do mago, tá na hora de aprender um pouco sobre classes agora.

#### Tá na hora de classes? Sala de aula?

Calma, em programação, classes são semelhantes a um molde para alguma coisa no dentro do teu programa, elas descrevem de uma maneira beeem genérica como aquela coisa deve ser, se comportar, o que ela deve possuir de atributos e o que ela faz. Até aqui tudo certo?

A partir deste molde, nós podemos criar a coisa que estamos querendo, ou no dialeto da computaria, instanciamos o nosso objeto.

O conceito todo de classe pode ser bem extenso e pode ser bem confuso, principalmente se você for um jovem padawan, então vou tentar manter super breve, mas por via de regra uma classe tem tres coisas bem importantes e interessantes:

- Atributos: O que a classe possui, semelhante a variaveis
- Construtor: Como que o objeto é criado, usado para alocar o objeto em questão na memória
- Métodos: O que a classe pode fazer/executar, bem semelhante a funções

Agora que sabemos um pouco como uma classe funciona, vamos pensar em como escrever ela em código. A forma de fazermos isso é através da palavra reservada `class`, seguido pelo nome da classe, que por convenção começa com letra maiuscula e em seguida a abertura de chaves `{}`.

Dentro das chaves, nós declaramos os nossos atributos, depois nosso construtor e por fim os métodos. Sempre que queremos referenciar algo dentro do objeto em questão, nós usamos o `this.`, o `this` atribui a um atributo local/escopado/privado dentro da classe um valor que vem de fora através do constructor ou outros métodos.

Após tudo isso, nós podemos finalmente criar nosso objeto. Para fazer isso, temos que atribuir ele a uma variavel e com o simbolo de igual, usamos a palavra reservada `new` para dizer que queremos uma nova `Classe()`.

O detalhe mais legal é que é justo nesta etapa que nós temos acesso ao constructor, podemos passar um ou mais parametros de maneira bem semelhante a uma função e com isso carregar os valores prontos para o nosso objeto.

```typescript
class Mago {
  nome: string;
  grimorio: Magia[] = [];

  constructor(nome: string) {
    this.nome = nome;
  }

  apresentar() {
    console.log(`Olá, sou ${this.nome}!`);
  }
}

const Elminster = new Mago('Elminster');
```

Viu só? `nome` e `magias` são atributos.

o `constructor` é onde criamos nosso objeto através da nomeclatura `new` e passamos para dentro do construtor o valor de nome. `const Elminster = new Mago('Elminster');`

O que vai acontecer quando você chamar `Elminster.apresentar()` embaixo da nossa variavel da classe?

### Sou eu, Bola de Fogo

O Elminster já sabe se apresentar, mas ainda não sabe nenhuma magia, como que a gente faz o querido aprender agora? Bora pensar aqui como fazer ele buscar conhecimento.

Para isso a gente vai criar um método chamado `procurarConhecimento()`. Esse método vai incluir uma magia nova no grimório do Elminster através do método `push` nativo do javascript/typescript.

```typescript
procurarConhecimento(magia: Magia) {
  this.grimorio.push(magia);
  console.log(`${this.nome} aprendeu ${magia.nome}.`);
}
```

Coloca esse método embaixo do `apresentar()`, pra ficar bonitinho.

Agora você já consegue utilizar o método com `Elminster.procurarConhecimento()` mas nota que pra funcionar, vai ter que passar um parametro. Coincidentemente a gente sabe duas magias pra ensinar pro Elminster: `bolaDeFogo` e `dardoDeChoque`. Podemos fazer a seguinte chamada: `Elminster.procurarConhecimento(bolaDeFogo)` e `Elminster.procurarConhecimento(dardoDeChoque)`.

Agora vamos criar outro método, vamos chamar ele de `magiasPreparadas()`. Ele não vai receber nenhum parametro e vai retornar todas as nossas magias conhecidas. Esse por enquanto podemos só fazer um console log para o atributo `this.grimorio`.

```typescript
magiasPreparadas() {
  console.log(this.grimorio)
}
```

#### Bonus

Mas e se o Elminster quiser MUITO esquecer uma magia? Digamos que ele tem medo que uma magia caia em mãos erradas?

Bom, nesse caso podemos escrever um método de amnésia para ele e evitar que o conhecimento caia nas garras de um poderoso Lich.

Esse exercicio eu vou deixar de dever de casa para quem quiser entender um pouco mais sobre estruturas de dados e como que pode-se resolver este exercicio.

```typescript
amnesia(magia: Magia) {
  // codigo para procurar a magia no grimorio e apagar da memória do Elminster
  // ...
  // ...
  console.log(`${this.nome} esqueceu ${magia.nome}.`)
}

```

Voltando ao tópico, precisamos fazer algo de util com nossas magias, certo? Que tal implementarmos um método para lançar magias.

Para isso vamos precisar de um método `lançar()`, o método pode receber um parametro ou não, depende de como queremos lidar com nosso pequeno programa.

Temos duas opções, uma delas é a de que sabemos de antemão todas as magias que ele pode usar e a outra é de que deviamos ser expostos as magias das quais temos conhecimento.

Vou abordar a segunda opção para dar um dinamismo maior e mostrar uma alternativa ao que já estamos trabalhando. A idéia é a de que possamos falar o seguinte em nosso codigo: `Elminster.lancar.bolaDeFogo()`, por exemplo.

Para isso precisamos:

- Construir uma função auxiliar `transformarEmChave()` para mapear as chaves do array de magias
- implementar o método `lancar()`
- retornar a magia em forma de ação

Vamos a primeira parte. Nossa função auxiliar vai receber um string e retornar uma string. Vamos precisar normalizar a string que recebemos, ou seja, transformar para lower case, remover os espaços e por fim retornar o resultado normalizado.

Mas como assim Matheus? Bora lá, eu te explico.

Nosso objetivo aqui é acessar o nosso grimório `grimorio: Magia[] = [];`. Para isso vamos fazer a função `transformarEmChave()` que recebe um argumento do tipo `string`.

```typescript
function transformarEmChave(nomeDaMagia: String) {
  // ...
}
```

Agora, vamos falar magia, porém magia da programação :) Vou mostrar alguns métodos para lidar com strings ou textos, isso é muito util para normalizar ou formatar coisas exatamente do jeito que se é esperado.

A primeira coisa que quero abordar é o `toLowerCase()`. Ele faz exatamente o que o nome propõe. Transforma algo que é em Maiscula ou MAIUSCULA ou maiUscula ou qualquer coisa que seja uma variação disso. Da mesma forma existe o seu oposto `toUpperCase()` que obviamente transforma para caixa alta.

```typescript
'Maiscula MAIUSCULA maiUscula'.toLowerCase();
'Bola de Fogo'.toUpperCase();

// 'maiscula maiuscula maiuscula'
// 'BOLA DE FOGO'
```

A segunda coisa é o `split()`. O split serve para separarmos uma cadeia de caracteres depois de determinada letra, ou caractere ou separador, ou qualquer coisa na verdade. Utilizamos ele passando um parametro separador, por exemplo `split(' ')` ou `split('|')`. O retorno deste método é um array.

```typescript
'Maiscula MAIUSCULA maiUscula'.split(' ');
'Bola de Fogo | Dardo Eletrico'.split('|');

// ['Maiscula', 'MAIUSCULA', 'maiUscula']
// ['Bola de Fogo ', ' Dardo Eletrico']
```

Até aqui é mamãozinho, né? A proxima etapa é onde começa a ficar um pouco arcano. Vou te mostrar o `map()`, mas pra isso tenho que falar um pouco de funções anonimas.

Funções anonimas são funções que não tem um identificador para serem chamadas, são instanciadas na hora, fazem o que tem que fazer e depois vão embora, são relevantes em um momento muito especifico do teu código.

> São conhecidas na boca miúda como funções lambda ou funçõezinhas de callback. - Aristoteles, depois de refatorar o backend da pedra de rosetta.

A primeira forma que poremos criar uma função anonima é assim:

```typescript
(function () {
  console.log('Sou uma função anonima :)');
})();
```

Mas nota que fica um pouco 'poluido' por causa dos parenteses, parece um pouco lisp, confuso né? Temos que declarar um primeiro nivel de parenteses e ai falar que é uma função sem nenhum nome e ai sim fazer o que precisamos, fechar o primeiro nivel de paranteses e ai sim outro par de parenteses.

A segunda forma, é um pouco mais simples, ainda precisamos do mesmo nivel de parenteses porém agora podemos simplesmente ignorar a nomeclatura `function()` e fazer uma simplificação:

```typescript
(() => {
  console.log('Sou uma função anonima com flechinha :)');
})();
```

O pulo do gato ai fica para a flechinha. Ela significa a mesma coisa que `function()`.

Podemos inclusive escrever funções normais desta forma.

```typescript
const nomeDoMago = () => {
  console.log(this.name);
};

// é a mesma coisa que:

function nomeDoMago() {
  console.log(this.name);
}
```

Tá, agora que adquiriu mais um pedaço de conhecimento ancestral, bora pro que interessa. Vamos juntar o que a gente aprendeu e somar com o fato de que o `map()` pode receber três parametros:

- currentValue
- index
- arr

O currentValue é o valor atual, o index é o indice especifico e o arr representa o array que vamos iterar.

```typescript
['Bola de Fogo']
  .map((p, i) => (i === 0 ? p : p[0].toUpperCase() + p.slice(1)))
  .join('');
```

Temos também o `slice()` e o `join()`

```typescript
['Bola de Fogo']
  .map((p, i) => (i === 0 ? p : p[0].toUpperCase() + p.slice(1)))
  .join('');
```

Juntando tudo o código fica assim:
(Ps: Vou usar a convenção de nomes que falei acima sobre os valores que `map()` aceita)

```typescript
// Converte uma string com espaços em camelCase. Ex: "bola de fogo" -> "bolaDeFogo"
return nome
  .toLowerCase() // normaliza tudo para minúsculas
  .split(' ') // quebra a string em um array de palavras usando o espaço como separador
  .map((currentValue, index) =>
    // Para cada palavra: a primeira (index 0) permanece minúscula
    // as demais têm a primeira letra convertida para maiúscula
    index === 0
      ? currentValue
      : currentValue[0].toUpperCase() + currentValue.slice(1),
  )
  .join(''); // junta tudo sem separador, formando a string em camelCase
```

Agora é tua vez de montar essa função toda, juntando os pedacinhos e ver como que vai ficar, como exercicio.

## Concluindo o nosso raciocinio

Se chegou até aqui, parabéns!! tem todos os conhecimentos arcanos para concluir o Elminster. Espero que você esteja saindo daqui com um pouco mais de sabedoria e conhecimento, tal qual o nosso querido :).

O nosso exercicio prático é uma pequena aplicaçaõ `CRUD`, sinonimo de `Create, Read, Update and Delete`. as operações base de praticamente todos os programas que você usa, assim como uma pequena pincelada em orientação a objetos.

Vou deixar o script completo com a minha resolução pra ti comparar e poder incrementar com algumas coisinhas a mais.

Ah, junto tem a função `amnésia` e `atualizarMagia` hehehe.

```typescript
// resolução
type Elemento = 'fogo' | 'gelo' | 'raio';

interface Magia {
  nome: string;
  elemento: Elemento;
  dano: number;
}

function transformarEmChave(nome: string): string {
  return nome
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .map((palavra, indice) =>
      indice === 0
        ? palavra
        : palavra[0].toUpperCase() + palavra.slice(1),
    )
    .join('');
}

class Mago {
  nome: string;
  grimorio: Magia[] = [];
  lancar: Record<string, () => void> = {};

  constructor(nome: string) {
    this.nome = nome;
  }

  apresentar(): void {
    console.log(`Olá, sou ${this.nome}!`);
  }

  procurarConhecimento(magia: Magia): void {
    this.grimorio.push(magia);
    this.prepararLancamento(magia);
    console.log(`${this.nome} aprendeu ${magia.nome}.`);
  }

  magiasPreparadas(): void {
    console.log(this.grimorio);
  }

  atualizarMagia(nomeAtual: string, magiaAtualizada: Magia): void {
    const indice = this.grimorio.findIndex(
      (magia) => magia.nome === nomeAtual,
    );

    if (indice === -1) {
      console.log(`${this.nome} não conhece ${nomeAtual}.`);
      return;
    }

    delete this.lancar[transformarEmChave(nomeAtual)];
    this.grimorio[indice] = magiaAtualizada;
    this.prepararLancamento(magiaAtualizada);

    console.log(`${this.nome} atualizou ${nomeAtual}.`);
  }

  amnesia(magia: Magia): void {
    const indice = this.grimorio.findIndex(
      (magiaConhecida) => magiaConhecida.nome === magia.nome,
    );

    if (indice === -1) {
      console.log(`${this.nome} não conhece ${magia.nome}.`);
      return;
    }

    this.grimorio.splice(indice, 1);
    delete this.lancar[transformarEmChave(magia.nome)];

    console.log(`${this.nome} esqueceu ${magia.nome}.`);
  }

  private prepararLancamento(magia: Magia): void {
    const chave = transformarEmChave(magia.nome);

    this.lancar[chave] = () => {
      console.log(
        `${this.nome} lançou ${magia.nome}! Causou ${magia.dano} de dano do elemento ${magia.elemento}.`,
      );
    };
  }
}

const bolaDeFogo: Magia = {
  nome: 'Bola de Fogo',
  elemento: 'fogo',
  dano: 30,
};

const dardoDeChoque: Magia = {
  nome: 'Dardo de Choque',
  elemento: 'raio',
  dano: 15,
};

const Elminster = new Mago('Elminster');

Elminster.apresentar();

Elminster.procurarConhecimento(bolaDeFogo);
Elminster.procurarConhecimento(dardoDeChoque);
Elminster.magiasPreparadas();

Elminster.lancar.bolaDeFogo();
Elminster.lancar.dardoDeChoque();

Elminster.atualizarMagia('Bola de Fogo', {
  nome: 'Bola de Fogo Maior',
  elemento: 'fogo',
  dano: 50,
});

Elminster.lancar.bolaDeFogoMaior();

Elminster.amnesia(dardoDeChoque);
Elminster.magiasPreparadas();
```
## Por enquanto é isso

Valeu demais, continua arrasando 🤘- Matheus.