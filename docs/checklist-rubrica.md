# Checklist da rubrica - Projeto Final T4

Fontes: enunciado oficial T4 (7 páginas, atualizado em 17/10/2026) e anotações do Departamento de Engenharia (1 página), lidos dos PDFs fornecidos por Fabiano.

Prazo atualizado informado por Fabiano: **16/11/2026 às 22h, horário de Brasília**. O enunciado contém a data antiga de 03/11/2026. A seção 4 define sete fases; a menção a seis fases na seção 5.1 é uma inconsistência editorial. Este projeto segue as sete fases.

Os itens abaixo representam a entrega completa; a estrutura inicial não conclui o pipeline.

## Fase 1: Análise Exploratória (EDA)

- [ ] Apresentar dimensões (linhas e colunas) e tipos das variáveis.
- [ ] Apresentar resumo estatístico das colunas numéricas com `.describe()`.
- [ ] Produzir pelo menos três gráficos analíticos fundamentados (exemplos do enunciado: histograma, barras da distribuição do alvo e correlação de Pearson).
- [ ] Interpretar os números e gráficos em Markdown, relacionando os padrões à estratégia de modelagem.

## Fase 2: Limpeza e Tratamento de Dados (Data Prep)

- [ ] Identificar e remover linhas duplicadas.
- [ ] Identificar ausentes e imputar por média ou mediana, justificando a escolha pela distribuição.
- [ ] Analisar outliers das variáveis explicativas com boxplots.

## Fase 3: Feature Engineering

- [ ] Tratar nulos antes da operação matemática.
- [ ] Criar uma coluna numérica combinando colunas existentes, sem valores inválidos.
- [ ] Documentar a fórmula e justificar a escolha no notebook e no vídeo.
- [ ] Considerar a sugestão `potencia = velocidade_rotacao_rpm * torque_nm`, ou justificar outra combinação. Esse produto não corresponde diretamente a potência em watts; documentar as unidades se utilizado.

## Fase 4: Divisão e Balanceamento dos Dados

- [ ] Separar preditoras X e alvo y (`falha_maquina`: 1 = falha, 0 = normal).
- [ ] Dividir em treino 80% e teste 20%, com `stratify=y`.
- [ ] Aplicar SMOTE ou Random Under Sampling exclusivamente ao treino após a divisão.
- [ ] Preservar o conjunto de teste sem reamostragem.

## Fase 5: Escalonamento de Variáveis (StandardScaler)

- [ ] Escalonar somente as variáveis contínuas destinadas ao KNN.
- [ ] Usar `fit_transform` no treino e apenas `transform` no teste.
- [ ] Manter os dados da Árvore de Decisão sem escalonamento e justificar no código sua independência da escala.

## Fase 6: Ajuste de Parâmetros e Combate ao Overfitting

- [ ] Treinar KNN com ao menos três valores ímpares de `n_neighbors` (ex.: 3, 5, 7).
- [ ] Treinar Árvore de Decisão com ao menos três valores de `max_depth` (ex.: 3, 5, None).
- [ ] Registrar acurácias de treino e teste para cada configuração dos dois modelos.
- [ ] Explicar em Markdown os pontos de sobreajuste e a configuração estável no teste.

## Fase 7: Avaliação da Acurácia e Veredito Final

- [ ] Calcular e exibir a acurácia no teste do melhor KNN e da melhor árvore.
- [ ] Comparar numericamente e justificar o modelo recomendado para a empresa.

## Cuidados com os dados e decisões pendentes

- [ ] Preservar o CSV original em `data/raw/manutencao_preditiva.csv`; efetuar transformações em memória.
- [ ] Excluir de X as colunas históricas `falha_twf`, `falha_hdf`, `falha_pwf`, `falha_osf` e `falha_rnf`, conforme as anotações da Engenharia: elas informam causas da quebra e provocam vazamento de informação.
- [ ] Avaliar a exclusão de `udi` e `id_produto`, descritos como identificadores, e documentar a decisão.
- [ ] Definir e justificar o tratamento da categoria `tipo` (L, M, H).
- [ ] Ajustar imputadores e demais transformações aprendidas somente no treino para evitar vazamento. Conciliar isso com a ordem expositiva das fases de limpeza e divisão.
- [ ] Definir a ordem entre escalonamento e reamostragem, especialmente se houver SMOTE e variáveis categóricas.
- [ ] Fixar sementes das operações aleatórias para reprodutibilidade.
- [ ] Discutir o limite da acurácia em dados desbalanceados e o uso do teste para escolher hiperparâmetros, exigido no enunciado; considerar validação interna ao treino e métricas complementares sem omitir a rubrica.

## Organização e documentação

- [ ] Entregar o código completo em um único notebook Jupyter com sete cabeçalhos Markdown.
- [ ] Acompanhar transformações, limpezas e treinamentos de textos que justifiquem as decisões.
- [ ] Criar `requirements.txt` com as bibliotecas utilizadas e respectivas versões.
- [ ] Utilizar caminhos relativos para os dados, sem diretórios pessoais absolutos no notebook.
- [ ] Documentar no README: nome, problema, escopo, técnicas e tecnologias, execução e melhorias possíveis.
- [ ] Verificar execução integral do notebook em ambiente configurado.

## GitHub e submissão - operações sob responsabilidade de Fabiano

- [ ] Manter repositório público no GitHub.
- [ ] Usar `develop` para integração e feature branches originadas nela para cada tarefa.
- [ ] Fazer commits pequenos com mensagens claras, sucintas e diretas.
- [ ] Preservar branches após os pull requests e integrar o resultado final em `main`.
- [ ] Submeter no AVA, na tarefa indicada no enunciado, os links do repositório e do vídeo.
- [ ] Respeitar o prazo atualizado e não alterar o projeto após a entrega até receber a nota; o PDF considera a última atualização do repositório como data final.
- [ ] Produzir solução autoral: plágio resulta em nota zero.

## Vídeo

- [ ] Gravar vídeo de até sete minutos, com rosto visível e boa iluminação.
- [ ] Explicar o objetivo e demonstrar o funcionamento.
- [ ] Explicar como executar e como as tarefas foram organizadas.
- [ ] Apresentar as branches criadas e seus objetivos.
- [ ] Discutir melhorias e justificar tecnicamente as escolhas.
- [ ] Não utilizar ferramenta de criação de vídeo com IA, conforme o enunciado.
- [ ] Disponibilizar no Google Drive como leitor para qualquer pessoa com o link; incluir o link no AVA (opcionalmente também no README).

## Pontuação da rubrica

| Critério | Pontuação máxima |
| --- | ---: |
| Vídeo com todos os tópicos | 2,0 |
| Branches e commits adequados | 0,5 |
| README completo | 0,5 |
| Fase 1 - EDA | 1,0 |
| Fase 2 - Data Prep | 1,0 |
| Fase 3 - Feature Engineering | 1,0 |
| Fase 4 - Divisão e balanceamento | 1,0 |
| Fase 5 - Escalonamento | 1,0 |
| Fase 6 - Ajuste e overfitting | 1,0 |
| Fase 7 - Avaliação e veredito | 1,0 |
| Total | 10,0 |

O projeto representa 60% da avaliação do módulo. A rubrica remete ao item 4.3 para README, mas a seção correspondente no documento é 5.2.
