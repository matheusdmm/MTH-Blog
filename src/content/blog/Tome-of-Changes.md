---
title: 'Tome of Changes'
description: 'Construi uma ferramenta pra comparar coisas do dnd 5e com o 5.5 e aprendi um monte de maluquice com isso.'
pubDate: 'May 09 2026'
tags: ['dev', 'dnd']
heroImage: 'https://images.unsplash.com/photo-1651677584025-6c844f0bd65c?q=80&w=1632&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
hidden: false
---

# Construí uma ferramenta para comparar o D&D 2014 com o D&D 2024 — e aprendi bastante no caminho

Tem uma situação que todo mestre de D&D conhece: você está no meio de uma sessão, alguém usa uma magia, e aí vem a pergunta que trava tudo.

_"Espera, Counterspell ainda funciona assim?"_

Aí começa a busca. Você abre o PHB de 2014, abre o de 2024, tenta lembrar qual versão o grupo está usando, procura no Reddit, lê três posts contraditórios, e quando você finalmente acha a resposta o momento já foi embora.

Foi exatamente essa frustração que me levou a construir o **Tome of Changes**.

---

## O problema

A edição 2024 do D&D não é uma nova edição — a Wizards chama de "revisão". Mas as mudanças são significativas o suficiente para causar confusão em qualquer mesa que misture jogadores de diferentes épocas, ou que esteja fazendo a transição.

Feitiços foram rebalanceados. Feats foram reformulados. As raças viraram "espécies" e perderam os bônus de atributo. O sistema de Exhaustion foi completamente redesenhado. A Counterspell agora exige um teste.

O problema não é que as mudanças sejam ruins — muitas são melhorias genuínas. O problema é que não existe uma forma fácil de ver **exatamente o que mudou**, lado a lado, sem abrir dois livros e fazer a comparação manualmente.

Então eu fiz isso.

---

## O que a ferramenta faz

O Tome of Changes busca qualquer entrada do SRD — uma magia, feat, criatura, condição, item mágico ou espécie — e exibe as duas edições comparadas em tempo real, direto no navegador.

Algumas coisas que considerei importantes desde o início:

**Diff palavra por palavra.** Não basta mostrar o texto dos dois lados. Eu queria que ficasse visível _exatamente_ onde o texto mudou — palavras adicionadas em verde, removidas em vermelho, dentro da própria frase. Pra isso implementei um algoritmo de LCS (Longest Common Subsequence) do zero, sem biblioteca, rodando inteiro no navegador.

**Tabela de estatísticas comparativa.** Para magias, criaturas e espécies, as mudanças mecânicas aparecem em uma tabela limpa antes do texto — nível, tempo de conjuração, alcance, CR, tamanho, velocidade. Se algum valor mudou entre as edições, a linha fica destacada.

**Mudanças detectadas.** Um resumo em linguagem natural no rodapé de cada card, listando o que a comparação encontrou de diferente.

**Links compartilháveis.** Cada busca tem sua própria URL. Você encontrou a comparação do Hex? Cola o link no Discord da sua mesa e todo mundo vê a mesma coisa.

**Favoritos.** Qualquer entrada pode ser salva com um clique — fica guardada no localStorage, persiste entre sessões, e tem uma página dedicada.

**Botão "Ask AI".** Um clique copia um prompt estruturado com todo o conteúdo da entrada — estatísticas, descrições completas das duas edições, mudanças detectadas — junto com uma instrução para o modelo explicar as alterações em **Português Brasileiro**. Funciona com Claude, ChatGPT, ou qualquer outro LLM.

**Tema claro e escuro.** Porque nem sempre o tema claro é a melhor opção.

---

## A stack

Sem backend. Sem banco de dados. Sem variáveis de ambiente pra configurar.

A ferramenta fala diretamente com a [Open5e API](https://open5e.com), que agrega os dados do SRD de ambas as edições de forma gratuita e aberta. Tudo o que acontece de complexo — o diff, a comparação de estatísticas, a geração do prompt — acontece no navegador.

| Camada     | Tecnologia                                                                  |
| ---------- | --------------------------------------------------------------------------- |
| Framework  | Vue 3 com Composition API e `<script setup>`                                |
| Build      | Vite 8                                                                      |
| Estilos    | Tailwind CSS v4 (configurado via `@theme` no CSS, sem arquivo de config JS) |
| Roteamento | Vue Router — cada busca é uma URL com estado                                |
| Dados      | Open5e API (v2 para a maioria das categorias)                               |

O Tailwind v4 foi uma escolha que valeu a pena. A configuração vive inteiramente num bloco `@theme` dentro do CSS — sem `tailwind.config.js`, sem muita frescura.

---

## O que aprendi

**Algoritmos clássicos ainda aparecem.** O LCS não é novidade — é o mesmo algoritmo usado pelo `diff` do Unix desde os anos 70. Mas implementá-lo do zero, com a grade O(mn) completa, e adaptá-lo pra operar em palavras em vez de caracteres, foi um exercício útil. Vale a pena entender o que está por baixo antes de instalar uma biblioteca.

```javascript
function diffWords(a, b) {
  const m = a.length,
    n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

  for (let i = m - 1; i >= 0; i--)
    for (let j = n - 1; j >= 0; j--)
      dp[i][j] =
        a[i] === b[j]
          ? dp[i + 1][j + 1] + 1
          : Math.max(dp[i + 1][j], dp[i][j + 1]);

  const tokens = [];
  let i = 0,
    j = 0;
  while (i < m || j < n) {
    if (i < m && j < n && a[i] === b[j]) {
      tokens.push({ text: a[i], type: 'same' });
      i++;
      j++;
    } else if (j < n && (i >= m || dp[i][j + 1] >= (dp[i + 1]?.[j] ?? 0))) {
      tokens.push({ text: b[j], type: 'added' });
      j++;
    } else {
      tokens.push({ text: a[i], type: 'removed' });
      i++;
    }
  }
  return tokens;
}

export function wordDiff(textA, textB) {
  const wordsA = (textA || '').split(/(\s+)/);
  const wordsB = (textB || '').split(/(\s+)/);
  return diffWords(wordsA, wordsB);
}
```

**APIs públicas têm inconsistências.** A estrutura dos dados do SRD de 2014 e 2024 na Open5e não é idêntica. Espécies de 2024 têm o conteúdo em um array de `traits` em vez de um campo `desc` no nível raiz. Criaturas de 2024 representam tipo e tamanho como objetos em vez de strings. Normalizar isso antes de passar os dados pra UI exigiu atenção — e é o tipo de coisa que testes de unidade teriam pego mais rápido se eu tivesse escrito.

**Localização parcial tem valor.** Não traduzi a interface — ela continua em inglês, porque os dados do SRD são em inglês e traduzi-los seria um projeto à parte. Mas oferecer o botão de Google Translate e o prompt pra LLM em pt-BR resolve 80% do problema pra um jogador brasileiro sem exigir manutenção de duas versões do conteúdo.

**Deploy de SPA precisa de configuração.** Aprendi isso da forma mais lenta possível: o Vue Router em modo history exige que o servidor redirecione todas as rotas para o `index.html`. No Vercel, isso é um `vercel.json` com uma linha. Sem ele, qualquer link compartilhado cai em 404.

---

## O que vem por aí

Algumas idéias que quero testar quando tiver tempo:

- Busca dentro da página de favoritos. Util quando você tem muita coisa salva e quer encontrar rapidamente.

---

## Onde encontrar

O projeto está no ar e é gratuito. Código aberto no GitHub.

- **Ferramenta:** [Tome of Changes](https://tomeofchanges.com)
- **Repositório:** [github.com/matheusdmm/Tome-of-Changes](https://github.com/matheusdmm/Tome-of-Changes)

Se você joga D&D e está navegando entre as edições, espero que ajude. Se você é desenvolvedor e quer contribuir ou tem sugestões, pull requests são bem-vindos.

Valeu demais, continua arrasando 🤘- Matheus.
