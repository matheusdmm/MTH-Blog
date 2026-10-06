# Editor local de posts

Interface local para listar, criar e editar os arquivos Markdown em `../src/content/blog`.

## Abrir com um clique

Dê dois cliques em **MTH-Editor.exe**. O editor abre no navegador padrão sem abrir uma janela do Windows Terminal. Não é necessário executar comandos. Ao fechar a última aba do editor, o processo encerra em alguns segundos.

Se o executável estiver dentro do projeto, ele encontra a pasta `src/content/blog` sozinho. Se estiver em outro lugar, clique em **Escolher pasta** e selecione a pasta que contém os arquivos `.md`. Você também pode clicar em **Informar caminho** e colar o caminho completo. O editor lembra da última pasta escolhida em `editor-settings.json`, ao lado do executável.

## Recriar o executável após alterar o código do editor

Na pasta `editor`, execute:

```powershell
bun run build
```

Não há instalação de pacotes no blog. Este comando só é necessário para quem modificar o código do editor e requer Bun e Go. O `package.json` e as dependências do blog não são alterados.

## Escrever

- Selecione um post no arquivo ou clique em **Novo post**.
- Escreva no modo **Visual** ou use **Markdown** para editar a sintaxe exata. O editor visual cobre a formatação comum; para Markdown complexo, prefira o modo Markdown.
- Preencha título, descrição e data. Tags são separadas por vírgulas.
- **Rascunho** fica ligado em posts novos. Desligue para publicar nas páginas do blog.
- Clique em **Salvar** ou use `Ctrl+S`. O editor avisa antes de fechar um post com alterações não salvas e detecta mudanças feitas no arquivo fora da interface.

> O feed RSS atual do blog não filtra posts com `hidden: true`. Se o blog for publicado enquanto há rascunhos, eles podem aparecer no feed. O editor não altera esse comportamento do blog.
