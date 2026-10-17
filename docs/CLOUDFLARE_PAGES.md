# Conectar ao Cloudflare Pages

O projeto é um painel estático. O build do Pages apenas empacota a versão já revisada; não recalcula os modelos e não instala dependências.

1. Abra https://dash.cloudflare.com/?to=/:account/workers-and-pages.
2. Escolha **Create application → Pages → Import an existing Git repository**.
3. Conecte o GitHub e autorize o aplicativo Cloudflare a acessar **FLeone2/mercado-automotivo-3**.
4. Selecione o repositório e configure:

| Campo | Valor |
|---|---|
| Project name | `mercado-automotivo-3` (se disponível) |
| Production branch | `main` |
| Framework preset | `None` |
| Root directory | Raiz do repositório; deixe o padrão |
| Build command | `python3 scripts/build-pages.py` |
| Build output directory | `dist` |
| Environment variables | Nenhuma necessária |

5. Clique em **Save and Deploy**. O Cloudflare informará a URL efetiva `*.pages.dev` após concluir o primeiro deploy. Não presumimos que um subdomínio esteja reservado.

Se o repositório não aparecer, abra as configurações do aplicativo Cloudflare Pages no GitHub, adicione o repositório à seleção permitida e volte à tela de conexão. A autorização da conexão GitHub deste chat não autoriza automaticamente o aplicativo do Cloudflare.

A pasta `dist` contém somente `index.html`, `404.html`, `_headers` e `data/`. Os dados e hashes CSP são preservados. Cada arquivo é conferido contra o limite de tamanho do Pages. Os scripts de desenvolvimento e os testes não são publicados nessa pasta.

A integração Git publica atualizações futuras da branch `main` automaticamente. Este projeto é separado da hospedagem do painel original.

Referências oficiais: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ e https://developers.cloudflare.com/pages/configuration/git-integration/.
