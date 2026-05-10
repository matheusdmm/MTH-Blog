---
title: 'Hero Scribe'
description: 'Ferramenta pra criar fichas de personagem de maneira simplificada no DnD 5e e 5.5.'
pubDate: 'May 12 2026'
heroImage: 'https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
hidden: false
---

Toda campanha de D&D começa da mesma forma: alguém abre o Player's Handbook, pega uma folha de papel e começa a preencher números. Ou vai ao D&D Beyond, cria uma conta, e descobre que metade das raças e classes que quer usar estão atrás de um paywall.

Foi aí que surgiu a ideia do **HeroScribe**.

## O problema que eu queria resolver

Eu jogo D&D há alguns anos e, toda vez que um amigo novo entra na mesa, o processo de criação de personagem vira um obstáculo desnecessário. As ferramentas online são boas, mas exigem cadastro, têm conteúdo bloqueado ou são pesadas demais pra quem só quer criar um guerreiro humano nível 1 e sair jogando.

Queria algo simples: você abre, cria, imprime ou exporta. Sem conta. Sem anúncio. Sem assinatura.

## A stack

Escolhi uma stack que me permitisse mover rápido sem me preocupar com infraestrutura:

- **Go** nas funções serverless do Vercel para os cálculos do personagem (modificadores, HP, CA, bônus de proficiência)
- **Vue 3** com Pinia no frontend — um wizard de múltiplos passos que guia o usuário do nome até os feitiços
- **Tailwind CSS** para o visual — um tema escuro com verde florestal e dourado que tenta remeter às capas dos livros antigos de RPG

A escolha do Go para o backend foi deliberada. A lógica de cálculo da ficha — HP pela fórmula do dado de vida, modificadores, bônus de proficiência por nível — vive 100% no servidor. O frontend nunca faz esse math, o que garante que as regras sejam aplicadas de forma consistente, independente do navegador.

## Construindo o wizard

O coração do HeroScribe é um wizard de 7 passos: Detalhes, Raça, Classe, Perícias, Atributos, Equipamentos e Magias. Cada passo muta um único objeto `draft` numa store Pinia centralizada. Quando o usuário chega ao final e clica em "Criar Personagem", esse draft é enviado ao backend, que devolve a ficha calculada.

A parte mais divertida de construir foi o **seletor de magias**. Ele consome a [Open5e API](https://api.open5e.com) em tempo real, paginando centenas de feitiços e filtrando pela classe e nível do personagem. Deu pra ver em tempo real como um Warlock de nível 5 já tem Magia do Pacto de 3º nível enquanto um Mago do mesmo nível nada tão além assim.

## Os desafios que eu não esperava

### O Vercel e o Go multi-arquivo

Em algum momento tentei extrair um helper compartilhado de CORS para um arquivo separado dentro do diretório `api/`. Faz todo sentido no papel: três handlers, todos precisam dos mesmos headers — por que repetir?

O problema é que o runtime do Vercel compila cada handler Go **de forma independente**. Ele não agrega os arquivos do diretório como um pacote. O resultado: o arquivo de helper não era incluído, a função `setCORSHeaders` ficava indefinida, e a criação de personagem quebrava silenciosamente.

A solução foi simples mas contraintuitiva: manter os headers inline em cada handler. Às vezes a duplicação certa é a duplicação que funciona.

### Exportar como PDF sem bibliotecas

Uma das features que mais gosto no HeroScribe é o **Export PDF**. A ficha gerada é bonita o suficiente pra imprimir e levar pra mesa. Mas chegar lá não foi trivial.

Tentei primeiro com `html2pdf.js`. O resultado era horrível: as fontes customizadas quebravam, o conteúdo era cortado no meio de seções, e o layout virava bagunça. Descartei em meia hora.

A solução foi usar `window.print()` com uma folha de estilos `@media print` cuidadosamente ajustada. O CSS de impressão força um layout de 3 colunas em A4, substitui as classes responsivas do Tailwind e esconde tudo que não precisa aparecer na ficha. Ficou mais limpo do que qualquer biblioteca teria entregado.

### O tema escuro com `bg-white` enterrado no código

Aparentemente, em algum momento eu havia colocado `bg-white` diretamente no componente principal do wizard. O Tailwind do projeto usa uma escala de cores invertida com variáveis CSS — `stone-900` no tema escuro é verde florestal, não cinza. Mas `bg-white` é sempre branco, em qualquer tema.

O resultado era um painel branco brilhante no meio de uma interface toda escura. Levou menos de um minuto pra corrigir, mas foi daqueles bugs que você só percebe quando para pra olhar de verdade.

## O que aprendi

**Manter a lógica de jogo no servidor foi a melhor decisão que tomei.** Quando precisei ajustar a fórmula de HP ou adicionar validação de atributos, mudei um arquivo Go. Não precisei me preocupar com o estado do frontend ou com casos de borda no cliente.

**Ferramentas simples escalam bem.** `localStorage` para salvar personagens, `window.print()` para PDF, `fetch` puro para as chamadas de API. Não há nada no HeroScribe que precise de um pacote extra pra existir.

**Código de qualidade é uma prática, não um estado.** Passei uma sessão inteira fazendo um cleanup estruturado: centralizei funções duplicadas, adicionei tratamento de erros nas chamadas fetch, removi componentes mortos, criei constantes no lugar de magic numbers. Nenhuma dessas mudanças adicionou uma feature nova — mas tornaram o código muito mais fácil de entender e modificar.

## O que vem por aí

O HeroScribe ainda tem espaço pra crescer. Quero adicionar suporte a subclasses, melhorar a experiência mobile e talvez permitir o compartilhamento de fichas via link. Por enquanto, ele faz o que precisa fazer: coloca um personagem na sua mão em menos de cinco minutos, sem burocracia.

Se você joga D&D 5e ou 5.5e (2024) e quiser testar, o projeto é aberto e está no ar. E se você é dev e quiser explorar o código, a stack é pequena o suficiente pra entender em uma tarde.

Boa sorte na próxima aventura.

Valeu demais, continua arrasando 🤘- Matheus.
