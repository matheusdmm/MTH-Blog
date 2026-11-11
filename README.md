# MATHEUSDMM

Personal blog and portfolio built with [Astro](https://astro.build).

## Curtidas

No fim de cada post, o leitor pode curtir, desfazer a curtida e ver a contagem. Um cookie anônimo identifica o navegador, sem conta. Limpar os cookies permite curtir de novo.

Para rodar o blog e o serviço de curtidas:

```sh
docker compose up -d --build
```

Abra [http://localhost:8080](http://localhost:8080). Para usar outra porta, defina `BLOG_PORT`. Se houver um proxy HTTPS na frente do Nginx, configure-o para enviar `X-Forwarded-Proto: https` para que o cookie seja marcado como seguro.

O banco `/data/likes.sqlite` fica no volume `likes-data`, que sobrevive a recriações dos contêineres. Preserve o volume ao atualizar o blog; `docker compose down -v` o apaga. O serviço de curtidas só fica acessível pela rota `/api/likes` do blog.

Para desenvolver sem Docker, rode `bun run dev`. O Astro serve o blog e a API de curtidas na mesma porta e usa a coleção de posts local. O banco local fica em `.data/likes.sqlite`.
