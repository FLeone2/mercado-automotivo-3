# Mercado Automotivo 3

Esta versão parte do retrato revisado `767f3f13a4ce0b7774f7475239587aead13c952b` de `FLeone2/mercado-automotivo`. A importação no novo repositório é o commit `0ddfdf625c984180fb7a2208705705b2040679c8`, descendente do README inicial do usuário. O repositório original não foi alterado.

## Organização e leitura

- Sete áreas principais: Panorama, Evolução, Concorrência, Segmentos, Territórios, Explorar e Contexto econômico. Dados e metodologia continua no acesso secundário.
- O mapa completo fica em Territórios; Panorama recebe um resumo das principais UFs e acesso à exploração territorial.
- Evolução tem Executiva, Composição, Crescimento e Detalhar. As análises detalhadas aparecem uma vez, em Detalhar. A auditoria de crescimento fica recolhida.
- Animações deixam a navegação principal e ficam disponíveis por reprodução contextual. A rota antiga `animations` permanece registrada, com todos os controles.
- Contexto econômico apresenta indicadores oficiais, seus históricos e a comparação descritiva de varejo e crédito real. Modelos, correlações, diagnósticos, previsões, sensibilidade espacial e simulações ficam no apêndice de Dados e metodologia. O ambiente anterior completo continua disponível ali.
- Formatos antes escondidos são promovidos conforme a pergunta: ranking mensal, slope, participação × crescimento, efeito mercado/participação, sazonalidade, composição, treemap, Marimekko e Sankey. Os 13 formatos permanecem em Explorar.

## Identidade visual

Cores persistem por identidade da marca, independentemente de posição, filtro ou seleção. Fiat usa azul aço; VW âmbar; BYD verde-mar; GM lavanda; Toyota oliva; Hyundai ameixa; Mitsubishi mantém vermelho. Outras marcas identificadas usam cores determinísticas, sem serem agrupadas sob a categoria “Outras”. Nomes, rótulos e tabelas complementam as cores. Há variantes claras/escuras; esta implementação não declara certificação de acessibilidade ou teste clínico de daltonismo.

## Novas análises

| Recurso | Implementação e limites |
|---|---|
| Top 3 marcas por UF | Três mapas com a mesma escala geográfica, um por colocação. Participações e volumes exatos na tabela; denominador contém todas as marcas da UF. |
| Espigões nacionais | Municípios de todo o recorte, uma projeção nacional comum, cor pela líder/uma cor/somente Mitsubishi, câmera por arraste ou controles, giro opcional e alternativa 2D. Sem remover volumes pequenos por limiar visual. Municípios sem vínculo ficam na tabela. |
| Estados em 3D | Altura por volume ou por mil residentes de 2026, cor da líder, rotação e alternativa 2D; escala do recorte explícita. |
| Rede × oportunidade | Mercado de SUVs ou picapes médias em cidades sem loja cadastrada. Raio e volume mínimo ajustáveis. Proximidade é distância entre centroides em linha reta, não trajeto rodoviário ou área comercial. Rede atual da base: 148 pontos, referência 07/07/2026. |
| Força regional | QL de qualquer marca por UF ou município. Referência nacional remove UF, município e região, preservando os filtros não territoriais. Bases locais menores que 100 são sinalizadas. |
| Crescimento territorial | Mesmos dias do ano anterior; variação percentual e absoluta. Base zero deixa percentual indisponível. |
| Tecnologias no tempo | Eletrificados e origem chinesa em leituras separadas, escala fixa 0–100%, seleção mensal e reprodução com movimento reduzido. Classificação desconhecida continua identificada. |
| Ritmo diário | Acumulado observado de um mês contra os mesmos dias do ano anterior. Acervo até setembro de 2026, sem atualização em tempo real. Não há calendário validado de feriados nem projeção de fechamento. |
| Mitsubishi por segmento | Picapes médias e grupos de SUVs por classificação BD exata. Volume e participação mensal; Top 8 mais modelos Mitsubishi, denominador com todos os modelos. Porte não garante equivalência de preço/propulsão. |
| Matriz de oportunidade | Volume do segmento × participação Mitsubishi por UF. Cortes na mediana de volume e participação do recorte, com quadrantes para investigação. Não é decisão automática de investimento. |
| Primeiros meses | Até seis modelos, 12 meses desde a primeira observação positiva no acervo completo. Isto não confirma lançamento comercial. O período global limita os valores exibidos; ausências ficam nulas. |
| HHI | Soma dos quadrados da participação mensal de todas as marcas × 10.000. Unidade é marca da fonte, não grupo econômico. Não mede sozinho intensidade competitiva. |
| Comparação entre anos | Meses alinhados por ano nos últimos 24 meses encerrados no mês final do recorte; sem prolongar lacunas. |

## Decisões deliberadas da avaliação

O waffle de participação pequena permanece disponível em Explorar em vez de ocupar o cartão executivo. Os mapas 3D são opcionais e mantêm alternativas 2D/tabelas. Não promovemos previsões que falharam na validação para destaque executivo e não liberamos superfície de resposta sem modelo validado. Não inventamos calendário útil, atualização diária, data de lançamento comercial ou geometria para completar lacunas.

## Dados, geografia e desempenho

Os cubos, o manifesto e os pacotes analíticos existentes são preservados byte a byte. Os novos cruzamentos são somas de registros efetivamente aceitos pelo pipeline de filtros; não são produtos de totais marginais. As chaves extras têm orçamento de memória e recusam combinações excedentes integralmente, com aviso para reduzir o recorte.

`data/geography/national-ufs.geojson` é a malha oficial nacional simplificada do IBGE, obtida pela API v3 com recorte interno de UFs. `v3-reference.json` usa a mesma projeção e os centroides de polígonos já auditados no diagnóstico espacial, ligados por código IBGE ao catálogo municipal. Estes centroides não são sedes oficiais, endereços de compradores ou lojas; podem cair fora de polígonos irregulares. Vínculos por nome/UF não encontrados ficam registrados na tabela.

Metadados de primeira observação são reproduzidos a partir de todos os cubos locais. Novas cargas exigem regeneração da referência e conferência dos limites territoriais/populacionais.

## Construção e verificação

```sh
python scripts/build-v3-reference.py  # somente quando atualizar fontes/metadata
python scripts/build-v3.py
for test in tests/*.test.cjs; do node "$test" || exit 1; done
python -m unittest discover -s tests -p 'test_*.py' -v
```

A dependência estatística experimental é a versão registrada em `scripts/requirements-scenarios.txt`. Em ambientes sem instalação global, use `PHASE23_DEPS` para indicar a instalação local de statsmodels e suas dependências.

O build final reaplica notas e atualiza os hashes CSP. A verificação em navegador deve cobrir as áreas, mudanças repetidas de filtros/visões, 2D/3D, controles por teclado, CSV, claro/escuro e largura móvel. Testes de componentes não substituem inspeção visual.
