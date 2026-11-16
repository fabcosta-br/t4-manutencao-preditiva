# Relatório técnico de auditoria - Bloco 02

Projeto Final T4 - Manutenção Preditiva. Execução auditada em 16/11/2026. Autoria acadêmica responsável de Fabiano Rodrigo Costa.

## Estado do projeto

Implementação registrada no commit `4057eae5a8fec4970714b3ba0ef9cbfdb8a47686`, originada em `feature/modelagem-avaliacao` e integrada a `develop` pelo PR #3, no merge `2cdc1aa`. As sete fases acadêmicas estão implementadas no notebook. O Bloco 01 conserva suas células de código e interpretações, com saídas recalculadas durante a execução integral.

Arquivos desta entrega incluem `projeto_final.ipynb`, `requirements.txt`, `docs/checklist-rubrica.md` e este relatório. O ambiente `.venv` recebeu imbalanced-learn e sua dependência sklearn-compat, nas versões registradas abaixo.

## Ambiente e reprodução

Kernel **T4 (.venv)**, Python **3.12.14**, executável `.venv\Scripts\python.exe`. O caminho do kernelspec foi comparado com o interpretador usado para instalar e verificar as dependências. `python -m pip check`, executado pelo Python da `.venv`, retornou `No broken requirements found.` Os imports e a execução dos pipelines passaram.

| Dependência | Versão instalada |
| --- | --- |
| imbalanced-learn | 0.14.2 |
| sklearn-compat | 0.1.6 |
| scikit-learn | 1.9.1 |
| numpy | 2.5.5 |
| scipy | 1.18.1 |
| pandas | 3.1.1 |
| matplotlib | 3.11.2 |
| seaborn | 0.13.2 |
| ipykernel | 7.4.0 |
| nbclient | 0.11.0 |
| nbformat | 5.11.1 |
| psutil | 7.2.2 |
| threadpoolctl | 3.8.0 |

As versões efetivas, incluindo dependências transitivas, estão fixadas em `requirements.txt`. scikit-learn, NumPy e SciPy conservaram as versões anteriores à instalação.

Para recriar em Python 3.12 no Windows, criar `.venv` e executar `./.venv/Scripts/python -m pip install -r requirements.txt`. Selecionar o interpretador `.venv/Scripts/python.exe` para o notebook e executar todas as células em ordem, a partir da raiz do repositório.

## Metodologia e prevenção de vazamento

Foram preservados os 10.000 registros, as 14 colunas e a divisão estratificada 80/20 com semente 42. A busca usa três dobras estratificadas, semente 42, `n_jobs=1` e uma thread numérica. Cada pipeline recebe `X_treino_bruto`. Medianas, moda, One-Hot Encoding, escala numérica do KNN e subamostragem são ajustados dentro de cada dobra. A potência mantém a fórmula `rpm * torque * 2π/60`, calculada após a imputação. A árvore utiliza valores numéricos sem padronização. A saída transformada tem nove colunas, incluindo seis atributos numéricos e três indicadores de categoria.

Os preditores permitidos são os cinco sensores e `tipo`, acrescidos da potência derivada. `udi`, `id_produto`, as cinco causas históricas e `falha_maquina` estão excluídos da entrada dos classificadores. As medianas, a moda e as médias do scaler foram verificadas contra as observações de treino de cada dobra. O teste recebe somente transformações já ajustadas e conserva valores, índices, rótulos e distribuição.

O critério de seleção é F1 médio da classe 1 na validação cruzada. As escolhas foram registradas antes de obter métricas de teste. A avaliação das seis configurações no teste atende à rubrica. Nenhuma configuração foi alterada a partir desses resultados.

## Distribuição e balanceamento

Na base completa há 9.661 registros normais (96,61%) e 339 falhas (3,39%). Random Under Sampling foi escolhido pelo custo baixo e pela seleção de observações reais, preservando categorias válidas. O descarte de dados majoritários é uma limitação reconhecida.

| Conjunto | Normais antes | Falhas antes | Normais após RUS | Falhas após RUS |
| --- | ---: | ---: | ---: | ---: |
| Treino final | 7729 | 271 | 271 | 271 |
| Treino da dobra 1 | 5152 | 181 | 181 | 181 |
| Treino da dobra 2 | 5153 | 180 | 180 | 180 |
| Treino da dobra 3 | 5153 | 181 | 181 | 181 |

O teste conserva 1.932 registros normais e 68 falhas, totalizando 2.000 registros. Os subconjuntos de validação conservam 2.667, 2.667 e 2.666 registros. O sampler participa de `fit` e é ignorado na previsão. Sua seleção foi verificada como subconjunto dos índices de treino de cada dobra.

## Configurações e resultados

Acurácia de treino original avalia todos os 8.000 registros anteriores à subamostragem. Acurácia de ajuste balanceado avalia as 542 observações efetivamente fornecidas ao classificador final.

| Modelo | Parâmetro | F1 CV médio | Desvio F1 CV | Acurácia treino original | Acurácia ajuste balanceado | Acurácia teste | Escolhido por CV |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| KNN | `{'modelo__n_neighbors': 3}` | 0.2505 | 0.0162 | 0.8281 | 0.9041 | 0.8425 | Não |
| KNN | `{'modelo__n_neighbors': 5}` | 0.2716 | 0.0260 | 0.8417 | 0.8948 | 0.8500 | Sim |
| KNN | `{'modelo__n_neighbors': 7}` | 0.2658 | 0.0244 | 0.8343 | 0.8893 | 0.8475 | Não |
| Árvore | `{'modelo__max_depth': 3}` | 0.2973 | 0.0165 | 0.8885 | 0.8690 | 0.8885 | Não |
| Árvore | `{'modelo__max_depth': 5}` | 0.3352 | 0.0432 | 0.8940 | 0.9446 | 0.8940 | Sim |
| Árvore | `{'modelo__max_depth': None}` | 0.2894 | 0.0059 | 0.8734 | 1.0000 | 0.8755 | Não |

## Métricas finais

| Modelo | Acurácia treino original | Acurácia teste | Precisão da falha | Recall da falha | F1 da falha |
| --- | ---: | ---: | ---: | ---: | ---: |
| KNN | 0.8417 | 0.8500 | 0.1588 | 0.7941 | 0.2647 |
| Árvore | 0.8940 | 0.8940 | 0.2209 | 0.8382 | 0.3497 |
| Baseline majoritario | 0.9661 | 0.9660 | 0.0000 | 0.0000 | 0.0000 |

As matrizes abaixo usam linhas reais [normal, falha] e colunas previstas [normal, falha].

| Modelo | TN | FP | FN | TP | Matriz |
| --- | ---: | ---: | ---: | ---: | --- |
| KNN | 1646 | 286 | 14 | 54 | `[[1646, 286], [14, 54]]` |
| Árvore | 1731 | 201 | 11 | 57 | `[[1731, 201], [11, 57]]` |
| Baseline majoritario | 1932 | 0 | 68 | 0 | `[[1932, 0], [68, 0]]` |

## Interpretação e recomendação

**KNN** apresentou as seguintes diferenças entre acurácia de treino original e teste.

- `{'modelo__n_neighbors': 3}` obteve 0.8281 no treino e 0.8425 no teste, diferença de -1.44 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 0.9041. F1 médio de validação igual a 0.2505.
- `{'modelo__n_neighbors': 5}` obteve 0.8417 no treino e 0.8500 no teste, diferença de -0.82 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 0.8948. F1 médio de validação igual a 0.2716.
- `{'modelo__n_neighbors': 7}` obteve 0.8343 no treino e 0.8475 no teste, diferença de -1.32 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 0.8893. F1 médio de validação igual a 0.2658.

A configuração `{'modelo__n_neighbors': 5}` foi escolhida pelo F1 interno de 0.2716. Nas configurações deste algoritmo, a acurácia do treino original ficou igual ou abaixo da acurácia de teste. Esse gap não evidencia sobreajuste. A interpretação também considera a acurácia das amostras efetivamente usadas no ajuste e o F1 de validação.

**Árvore** apresentou as seguintes diferenças entre acurácia de treino original e teste.

- `{'modelo__max_depth': 3}` obteve 0.8885 no treino e 0.8885 no teste, diferença de 0.00 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 0.8690. F1 médio de validação igual a 0.2973.
- `{'modelo__max_depth': 5}` obteve 0.8940 no treino e 0.8940 no teste, diferença de 0.00 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 0.9446. F1 médio de validação igual a 0.3352.
- `{'modelo__max_depth': None}` obteve 0.8734 no treino e 0.8755 no teste, diferença de -0.21 pontos percentuais. Acurácia nas amostras balanceadas de ajuste 1.0000. F1 médio de validação igual a 0.2894.

A configuração `{'modelo__max_depth': 5}` foi escolhida pelo F1 interno de 0.3352. Nas configurações deste algoritmo, a acurácia do treino original ficou igual ou abaixo da acurácia de teste. Esse gap não evidencia sobreajuste. A interpretação também considera a acurácia das amostras efetivamente usadas no ajuste e o F1 de validação.

A árvore sem limite atingiu 1.0000 nas amostras usadas para o ajuste, enquanto seu F1 de validação foi 0.2894, abaixo de 0.3352 para a árvore selecionada. Essa perda de generalização com maior capacidade é evidência de sobreajuste. A acurácia no treino original inclui registros descartados pelo sampler e, por isso, não é a mesma medida da acurácia nas amostras efetivamente usadas no ajuste. Na avaliação do treino original, nenhum dos modelos apresentou vantagem positiva sobre o teste. O KNN teve F1 limitado, sem evidência de sobreajuste por esse gap. A árvore de profundidade 3 teve F1 interno inferior ao de profundidade 5, compatível com limitação de capacidade nessa comparação. A árvore selecionada manteve acurácias de treino original e teste iguais. Nenhum hiperparâmetro foi revisto após a comparação de teste.

**KNN**, com `{'modelo__n_neighbors': 5}`, alcançou F1 médio de validação 0.2716. Na avaliação final, acurácia de treino 0.8417, acurácia de teste 0.8500, precisão da falha 0.1588, recall 0.7941 e F1 0.2647. Houve 14 falsos negativos e 286 falsos positivos no teste.

**Árvore**, com `{'modelo__max_depth': 5}`, alcançou F1 médio de validação 0.3352. Na avaliação final, acurácia de treino 0.8940, acurácia de teste 0.8940, precisão da falha 0.2209, recall 0.8382 e F1 0.3497. Houve 11 falsos negativos e 201 falsos positivos no teste.

O baseline majoritário obteve acurácia 0.9660, recall 0.0000 e F1 0.0000. Sua acurácia elevada acompanha a prevalência de funcionamento normal e oculta a ausência de detecção de falhas.

**Recomenda-se Árvore**, pela maior média de F1 de validação cruzada, critério definido e aplicado antes do acesso às métricas de teste. A maior acurácia final entre os dois modelos selecionados foi observada em Árvore, com 0.8940. Essa comparação atende à rubrica e mantém a escolha de hiperparâmetros já registrada. Os falsos negativos representam falhas que passariam sem alerta, enquanto os falsos positivos gerariam inspeções. Os custos relativos desses erros precisam ser definidos pela operação antes de uma implantação.

**Limitações e melhorias.** O teste contém 68 falhas e a divisão é aleatória. Não foi demonstrada antecedência temporal de horas ou dias. Random Under Sampling reduziu o treino final para 542 registros e descartou grande parte da classe normal. A EDA foi realizada na base completa conforme a rubrica, e as seis configurações foram expostas ao teste para relatório. A decisão foi registrada previamente, mas novas otimizações exigiriam uma avaliação independente. Como continuidade, ampliar os dados, verificar divisões por tempo e equipamento quando existirem metadados apropriados, estimar incerteza das métricas e quantificar custos dos erros. As transformações são reajustadas dentro de cada dobra, incluindo imputação, engenharia, codificação, escala do KNN e balanceamento.

## Execução e validações

A execução final passou pelas **15 células de código**, com contagem sequencial de 1 a 15 e **zero exceções**. Tempo real integral, incluindo inicialização do kernel, igual a **17.07 s**. O intervalo medido dentro do kernel foi de 14.07 s. Tempo de CPU do kernel igual a 11.25 s, RSS final de 243.57 MiB e pico de memória de 245.43 MiB. Essas medidas correspondem à execução final e variam conforme cache e máquina.

- Matrizes de entrada com dimensões compatíveis e valores finitos.
- Índices e rótulos alinhados, com treino e teste disjuntos.
- Transformações aprendidas exclusivamente no treino de cada dobra.
- Balanceamento exclusivo nos treinos e presença apenas de preditores permitidos.
- Categorias desconhecidas e nulos artificiais tratados pelos transformadores ajustados.
- Reajuste dos dois modelos finais com as mesmas sementes produziu as mesmas seleções e previsões.
- CSV, conjunto de teste e código do Bloco 01 preservados.

SHA-256 do CSV antes e depois da execução igual a `21f0032f6a94bacc897cbc7a26de9ffdc3fcd68adbc087db267a2d36d2dfea74`.

## Ocorrências e pendências

A primeira tentativa de instalação foi bloqueada pela rede do sandbox (WinError 10013). A instalação autorizada foi concluída com a liberação de rede. Na primeira execução, o teste de nulos artificiais tentou inserir NaN em uma coluna int64 da cópia de verificação. A correção converteu essa cópia numérica para float, seguida de nova execução integral. O diagnóstico de ajuste balanceado e a apresentação dos gráficos foram complementados, seguidos de execução integral. As dependências permaneceram nas versões registradas. Jupyter emitiu avisos de adaptação do loop de eventos e transporte TCP local durante a inicialização, sem falha na execução final.

O Bloco 02 foi revisado e integrado em `develop`. A documentação executiva foi preparada no Bloco 03 e aguarda revisão e versionamento. Como melhorias do experimento, ampliar a avaliação independente, estimar incerteza e levantar custos dos erros. A consolidação da versão final em `main` e a submissão dos links continuam pendentes no checklist.

A publicação do Bloco 02 está registrada no commit técnico citado neste relatório. A revisão documental do Bloco 03 preserva código, resultados e evidências de execução.
