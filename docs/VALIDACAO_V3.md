# Validação da versão 3

- 58 suítes JavaScript passaram, incluindo a nova conferência dos cruzamentos contra cubos reais de setembro de 2026.
- 109 testes Python passaram. O teste SARIMAX foi executado com statsmodels 0.15.0 e patsy instalados em diretório temporário, sem alterar dados ou modelos publicados.
- Build final: JavaScript dos dois scripts executáveis analisado e hashes CSP atualizados.
- Chromium: Panorama, ritmo diário, comparação de anos, todos os oito painéis comerciais, dez opções territoriais, contexto econômico e apêndice percorridos sem erros de execução.
- Top 3: 81 contornos estaduais, três mapas completos.
- Espigões: municípios associados desenhados, vínculos ausentes preservados na tabela.
- 3D: mudança de câmera e escolha de taxa por população verificadas.
- Largura móvel de 390 px: sem transbordamento horizontal da página; mapas empilhados e opções locais com rolagem.
- Os cubos, o manifesto e os pacotes analíticos originais permanecem inalterados.

A checagem de navegador é local. O novo repositório ainda precisa de uma integração própria de hospedagem para expor uma URL do painel; a integração Cloudflare do projeto original não é transferida com o Git.

Reprodução dos testes de navegador: iniciar um servidor HTTP no diretório do projeto e executar `node tests/browser-v3.cjs http://127.0.0.1:8765/`, com Playwright e Chromium disponíveis. O script exporta capturas e o CSV de conferência para `/tmp`.
