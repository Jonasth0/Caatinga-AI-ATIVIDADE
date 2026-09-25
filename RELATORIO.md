# Caatinga.AI — Sprint 1
## Relatório técnico — Inteligência Artificial

**Disciplina:** Inteligência Artificial  
**Instituição:** UniRios  
**Semestre:** 2026.2  
**Integrante 1:** Jonas Thiago — matrícula 24114049  
**Integrante 2:** Diego Delgado — matrícula 24114033  
**Matrícula utilizada como semente dos experimentos:** 24114049

---

# 1. Parte 1 — O agente antes do código

## 1.1 PEAS do Caatinga.AI

| Elemento | Descrição |
|---|---|
| **Performance** | Minimizar o custo do caminho até o ponto de coleta, mantendo a chegada ao objetivo e atendendo às prioridades de inspeção. |
| **Environment** | Pomar de manga representado por uma grade, com talhões livres (`.`), talhões de solo encharcado/irrigação (`~`) e posições bloqueadas (`#`). |
| **Actuators** | Movimentação ortogonal para Norte, Sul, Oeste ou Leste e indicação/priorização dos talhões que devem ser inspecionados. |
| **Sensors** | Mapa/grade do pomar e sensor óptico que produz alertas de suspeita de pragas. |

A missão de navegação parte de `(0,0)` e deve chegar a `(11,11)`. O custo é a soma dos custos dos talhões nos quais o agente entra, sem contabilizar o talhão inicial.

## 1.2 Classificação do ambiente

| Dimensão | Classificação | Evidência / justificativa |
|---|---|---|
| **Observável** | Parcialmente observável | O mapa da grade fornece a estrutura do ambiente, mas a presença de pragas é inferida por um sensor com falsos positivos e falsos negativos. |
| **Determinístico** | Determinístico para a navegação | Para um estado e uma ação de movimento, a transição na grade é determinada. A geração do pomar também é determinada pela semente. |
| **Sequencial** | Sequencial | Cada movimento altera a posição do agente e influencia os estados futuros. |
| **Estático** | Tratado como estático | O enunciado não informa mudanças de obstáculos ou custos durante a execução. A grade é gerada antes da busca e permanece fixa. |
| **Discreto** | Discreto | Os estados são posições inteiras da grade e as ações são quatro movimentos ortogonais. |
| **Agente único** | Agente único | O cenário descreve um único agente percorrendo o pomar. |

As duas dimensões mais discutíveis são **observabilidade** e **estaticidade**. Para observabilidade, seria necessário saber se o agente recebe o estado real de infestação ou apenas leituras imperfeitas do sensor. Para estaticidade, seria necessário saber se obstáculos, custos do terreno ou estado das pragas podem mudar durante a missão.

## 1.3 Tipo de agente

Foi escolhido o **agente baseado em utilidade**.

A escolha se deve à necessidade de considerar diferentes consequências mensuráveis, como chegar ao objetivo, evitar posições bloqueadas, reduzir o custo de deslocamento e atender às prioridades de inspeção. Uma função de utilidade permite combinar esses objetivos.

## 1.4 Métrica perversa

Uma métrica problemática seria maximizar apenas a quantidade de talhões suspeitos inspecionados, sem exigir a chegada ao objetivo.

Nesse caso, o agente poderia permanecer em uma região próxima do início, acumulando inspeções, e abandonar a missão principal.

A correção é tornar a chegada ao objetivo uma condição obrigatória e otimizar custo e inspeções somente entre soluções que cumprem a missão.

---

# 2. Parte 2 — Formulação e busca cega

## 2.1 Formulação do problema

**Estado inicial:** `(0,0)`.

**Ações:** mover uma posição para Norte, Sul, Oeste ou Leste, desde que a posição esteja dentro da grade e não seja bloqueada.

**Modelo de transição:** a ação altera a posição atual para o talhão vizinho permitido.

**Teste de objetivo:** atingir `(11,11)`.

**Custo do caminho:** soma dos custos dos talhões nos quais o agente entra. Talhões `.` custam 1 e talhões `~` custam 4; o talhão inicial não é contabilizado.

A ordem de expansão de vizinhos utilizada foi:

**Norte → Sul → Oeste → Leste**

Essa ordem foi mantida de forma consistente entre as estratégias.

## 2.2 Espaço de estados

Para uma grade `n × n`, existem no máximo:

`n²`

posições representáveis.

Para `n = 12`:

`12² = 144 estados`.

O número de estados efetivamente alcançáveis pode ser menor devido aos bloqueios.

## 2.3 BFS, DFS e UCS

Resultados da execução com a semente **24114049**:

| Estratégia | Custo | Passos | Nós expandidos | Fronteira máxima | Tempo (ms) |
|---|---:|---:|---:|---:|---:|
| BFS | 49 | 22 | 121 | 13 | 0,2505 |
| DFS | 123 | 48 | 83 | 37 | 0,1892 |
| UCS | **40** | 22 | 120 | 15 | 0,3825 |

A **BFS** encontrou uma rota de 22 passos, mas com custo 49. A **UCS** encontrou também 22 passos, porém com custo 40. Isso ocorre porque a BFS minimiza a quantidade de passos e não o custo acumulado quando existem custos diferentes de entrada.

No cenário, entrar em `.` custa 1 e entrar em `~` custa 4. Portanto, a BFS somente teria garantia de optimalidade em custo se todas as ações tivessem o mesmo custo.

A **DFS** expandiu menos nós que BFS e UCS, mas encontrou uma solução com custo 123 e 48 passos. Assim, menor quantidade de expansões não implica menor custo de solução.

## 2.4 Escalabilidade

Foi realizado um experimento adicional com BFS, DFS, UCS e A* Manhattan em grades de 12×12 até 800×800.

| n | Estratégia | Custo | Passos | Expandidos | Fronteira máx. | Tempo (s) |
|---:|---|---:|---:|---:|---:|---:|
| 12 | BFS | 55 | 22 | 115 | 13 | 0,000153 |
| 12 | DFS | 62 | 26 | 96 | 36 | 0,000121 |
| 12 | UCS | 34 | 22 | 111 | 23 | 0,000220 |
| 12 | A* Manhattan | 34 | 22 | 92 | 26 | 0,000202 |
| 40 | BFS | 174 | 78 | 1287 | 41 | 0,001597 |
| 40 | DFS | 987 | 432 | 835 | 403 | 0,001046 |
| 40 | UCS | 107 | 80 | 1278 | 57 | 0,002461 |
| 40 | A* Manhattan | 107 | 80 | 799 | 106 | 0,001752 |
| 100 | BFS | 426 | 198 | 8016 | 101 | 0,008582 |
| 100 | DFS | 4427 | 2036 | 4869 | 2280 | 0,006396 |
| 100 | UCS | 286 | 202 | 8015 | 140 | 0,016203 |
| 100 | A* Manhattan | 286 | 202 | 7372 | 336 | 0,016187 |
| 200 | BFS | 800 | 398 | 31897 | 192 | 0,034464 |
| 200 | DFS | 16239 | 7356 | 18710 | 7251 | 0,025655 |
| 200 | UCS | 556 | 406 | 31894 | 309 | 0,065512 |
| 200 | A* Manhattan | 556 | 406 | 30427 | 695 | 0,073360 |
| 400 | BFS | 1824 | 798 | 127964 | 371 | 0,181603 |
| 400 | DFS | 76655 | 34874 | 61390 | 34561 | 0,105776 |
| 400 | UCS | 1118 | 842 | 127964 | 593 | 0,602375 |
| 400 | A* Manhattan | 1118 | 842 | 125396 | 1503 | 0,563304 |
| 800 | BFS | 3527 | 1598 | 511304 | 737 | 0,952996 |
| 800 | DFS | 305170 | 138772 | 256421 | 137778 | 0,543769 |
| 800 | UCS | 2156 | 1652 | 511303 | 1252 | 1,559846 |
| 800 | A* Manhattan | 2156 | 1652 | 490690 | 3449 | 1,584487 |

Nenhuma estratégia atingiu o limite de 60 segundos nem apresentou `MemoryError` ou `RecursionError` até 800×800.

Assim, **800×800 é o maior tamanho efetivamente testado**, não um ponto de falha da máquina.

---

# 3. Parte 3 — Busca informada

## 3.1 A* e heurísticas

Foram utilizadas:

- `h1(n) = 0`
- `h2(n) = Manhattan`
- `h3(n) = 4 × Manhattan`

Resultados da semente 24114049:

| Heurística | Custo | Passos | Nós expandidos | Fronteira máxima |
|---|---:|---:|---:|---:|
| h1 = 0 | 40 | 22 | 120 | 15 |
| h2 = Manhattan | 40 | 22 | 115 | 18 |
| h3 = 4 × Manhattan | 40 | 22 | 27 | 23 |

### h1 = 0

Como `h1(n)=0`:

`f(n) = g(n)`.

Logo, A* com h1 se comporta como UCS. Os resultados confirmam isso: ambas encontraram custo 40 e expandiram 120 nós.

### h2 = Manhattan

A heurística é:

`h2(n) = |linha - linha_objetivo| + |coluna - coluna_objetivo|`.

Cada movimento ortogonal reduz a distância de Manhattan em no máximo 1 e cada entrada válida custa pelo menos 1. Portanto, a distância de Manhattan nunca supera o custo real mínimo restante.

Logo:

`h2(n) <= custo_ótimo_restante(n)`

e h2 é admissível.

### h3 = 4 × Manhattan

h3 não é admissível em geral porque pode superestimar o custo restante.

Um contraexemplo concreto no pomar da semente 24114049 é o estado `(10,11)` com objetivo `(11,11)`.

A distância de Manhattan é 1:

`Manhattan = 1`

Logo:

`h3 = 4 × 1 = 4`.

Porém, o objetivo `(11,11)` é `.` e custa 1 para entrar. Assim:

`h3 = 4 > 1 = custo real restante`.

Portanto, h3 pode superestimar e não possui garantia de admissibilidade.

## 3.2 Comparação entre h3 e UCS

Na execução:

- UCS: custo 40 e 120 nós expandidos;
- A* h3: custo 40 e 27 nós expandidos.

A redução observada nas expansões foi:

`(120 - 27) / 120 × 100 = 77,5%`.

Entretanto, o fato de h3 ter encontrado o mesmo custo nessa execução não prova sua admissibilidade ou optimalidade geral.

Uma organização poderia aceitar uma heurística não admissível quando houver um limite operacional de tempo para resposta e uma tolerância previamente definida para aumento de custo. Essa decisão deve ser baseada em uma regra de negócio explícita, e não apenas na observação de que h3 foi mais rápida em uma instância.

## 3.3 Busca local

Foi utilizado `K = 15`, com 30 execuções de cada método.

| Método | Média | Desvio-padrão | Melhor resultado |
|---|---:|---:|---:|
| Subida de encosta | 34,6 | 5,50 | 45 |
| Têmpera simulada | 60,0 | 0,00 | 60 |

A têmpera simulada registrou **1043 aceitações de piora** nas 30 execuções.

Isso constitui evidência experimental de que o algoritmo aceitou movimentos para estados de qualidade inferior, conforme o mecanismo previsto para escapar de ótimos locais.

---

# 4. Parte 4 — Regras e incerteza

## 4.1 Sistema especialista

O sistema especialista utiliza regras explícitas SE...ENTÃO e encadeamento para trás.

A função `provar()` recebe uma conclusão, verifica se ela está entre os fatos e, caso contrário, procura regras cuja conclusão seja o objetivo. As condições da regra são então provadas recursivamente.

A base atual possui **oito regras**:

- **R1:** SE `armadilha_positiva` E `umidade_alta` ENTÃO `risco_infestacao`.
- **R2:** SE `risco_infestacao` E `dias_desde_pulverizacao_maior_14` ENTÃO `inspecionar_prioridade_alta`.
- **R3:** SE `armadilha_positiva` E `umidade_baixa` E `nao_ha_risco_adicional` ENTÃO `inspecionar_prioridade_media`.
- **R4:** SE `armadilha_negativa` ENTÃO `inspecionar_prioridade_baixa`.
- **R5:** SE `risco_infestacao` E `talhao_encharcado` ENTÃO `inspecionar_prioridade_alta`.
- **R6:** SE `inspecionar_prioridade_alta` ENTÃO `manejo_urgente`.
- **R7:** SE `armadilha_positiva` E `umidade_baixa` E `dias_desde_pulverizacao_maior_14` ENTÃO `risco_infestacao`.
- **R8:** SE `intervalo_minimo_aplicacao_nao_atingido` ENTÃO `nao_autorizar_aplicacao`.

As regras R7 e R8 foram adicionadas explicitamente para tratar casos adicionais e manter as decisões auditáveis.

O mecanismo também mantém um conjunto de objetivos visitados. Caso um objetivo seja encontrado novamente durante uma prova, o sistema registra `CICLO EVITADO` e interrompe aquela ramificação.

## 4.2 Quebra e correção da base

Foi utilizado como caso de teste:

```text
armadilha_positiva
umidade_baixa
dias_desde_pulverizacao_maior_14
```

### Antes da correção

Para reproduzir a base quebrada, a função `regras_sem_correcao()` remove R7.

A conclusão desejada é:

`manejo_urgente`

Para chegar a ela, é necessário provar:

`manejo_urgente`
→ R6
→ `inspecionar_prioridade_alta`
→ R2
→ `risco_infestacao`

Sem R7, a prova de `risco_infestacao` depende de R1:

`armadilha_positiva` + `umidade_alta`

Porém, o caso possui `umidade_baixa`. Portanto, a prova falha.

### Correção

A R7 foi adicionada:

```text
SE armadilha_positiva
E umidade_baixa
E dias_desde_pulverizacao_maior_14
ENTÃO risco_infestacao
```

Depois da correção, o encadeamento pode seguir:

```text
R7 → risco_infestacao
R2 → inspecionar_prioridade_alta
R6 → manejo_urgente
```

Assim, a conclusão passa a ser demonstrável.

A correção não elimina as regras anteriores: ela adiciona uma condição explícita para um caso legítimo que não era coberto pela base original.

## 4.3 Bayes

Para a execução da matrícula **24114049**, o programa produziu:

- prevalência: **0,0118**;
- sensibilidade: **0,95**;
- taxa de falso positivo: **0,03**;
- talhões por semana: **2000**.

O programa calcula:

`P(+) = sensibilidade × prevalência + falso_positivo × (1 - prevalência)`

e:

`PPV = (sensibilidade × prevalência) / P(+)`.

O resultado obtido foi:

**PPV = 29,37%.**

Portanto, aproximadamente 29,37% dos alertas positivos correspondem a infestação segundo os parâmetros do modelo.

### Falsos a cada 100 alertas

O complemento do PPV é:

`100 - 29,37 = 70,63`.

Portanto:

**70,63 falsos a cada 100 alertas positivos.**

### Falsos positivos por semana

O programa calculou:

**23,70 falsos positivos por semana.**

Com 12 minutos por inspeção:

**4,74 horas por semana.**

### Sensibilidade de 99,9%

Mantendo os demais parâmetros e aumentando a sensibilidade para 99,9%, o programa calculou:

**PPV = 29,99%.**

O resultado mostra que aumentar apenas a sensibilidade produz uma mudança pequena no PPV enquanto a taxa de falso positivo permanece em 3%.

## 4.4 Regra de decisão auditável

A regra que transforma a conclusão de prioridade em ação deve permanecer explícita:

> Se `inspecionar_prioridade_alta`, então `manejo_urgente`.

A vantagem de manter essa decisão como regra explícita é permitir que a organização identifique quais condições produziram a decisão e possa auditar o caminho lógico utilizado pelo sistema.

---

# 5. Parte 5 — Auditoria do laudo do fornecedor

## Afirmação 1 — A* com h3 é sempre ótimo

**Veredito: incorreta.**

A garantia de optimalidade do A* depende das propriedades da heurística. A heurística utilizada pelo fornecedor, `4 × Manhattan`, pode superestimar.

No próprio pomar, para `(10,11)` até `(11,11)`, h3 vale 4, enquanto o custo real restante é 1.

Na execução, h3 encontrou custo 40, igual ao UCS, mas esse resultado não fornece uma garantia geral.

## Afirmação 2 — A* Manhattan reduziu o custo em 38%

**Veredito: não confirmado pelos dados desta execução.**

Os valores medidos foram:

- BFS: 49;
- A* Manhattan: 40.

A redução foi:

`(49 - 40) / 49 × 100 ≈ 18,37%`.

Portanto, a execução realizada mede aproximadamente **18,37%**, e não 38%.

## Afirmação 3 — Sensibilidade de 99% significa que 99% dos alertas são verdadeiros

**Veredito: incorreta.**

Sensibilidade representa `P(+|I)`, enquanto a probabilidade de um alerta positivo representar uma infestação é o PPV, `P(I|+)`.

No experimento, o PPV foi **29,37%**.

Portanto, os dois indicadores não podem ser tratados como equivalentes.

## Afirmação 4 — Dois positivos garantem confiança superior a 99%

**Veredito: não demonstrada com os parâmetros fornecidos.**

Para calcular a probabilidade posterior de dois resultados positivos, é necessário conhecer como os dois testes se relacionam estatisticamente.

Sob a hipótese adicional de independência condicional, o cálculo seria:

`P(I|++) = (s²p) / [(s²p) + (f²(1-p))]`.

Com os parâmetros desta execução (`s=0,95`, `f=0,03`, `p=0,0118`), o valor fica abaixo de 99%.

Sem a hipótese de independência condicional, os parâmetros de uma única medição não são suficientes para determinar o novo PPV.

## Afirmação 5 — DFS é suficiente porque usa pouca memória

**Veredito: insuficiente como justificativa para o problema completo.**

A DFS pode ter vantagens de memória em determinados espaços de busca, mas isso não garante uma solução de menor custo.

Na execução da semente 24114049:

- DFS: custo **123**, 48 passos;
- UCS: custo **40**, 22 passos.

Além disso, a fronteira máxima medida foi 37 para DFS e 15 para UCS nesta instância.

Portanto, a escolha de DFS não pode ser justificada somente por uma alegação genérica de memória quando o objetivo do problema também é minimizar o custo da rota.

## Recomendação à diretoria

A recomendação é condicionar a adoção do sistema à validação das garantias anunciadas pelo fornecedor. Deve-se exigir que a rota ótima utilize condições teóricas adequadas, que os indicadores do sensor diferenciem sensibilidade de PPV e que afirmações sobre testes repetidos explicitem suas hipóteses estatísticas. Também devem ser definidos limites de tempo e custo aceitáveis para soluções não necessariamente ótimas.

---

# 6. Parte 6 — Uso de IA

O uso de ferramentas de IA deve ser documentado no arquivo `ANEXO_IA.md`, conforme exigido no enunciado.

O anexo deve registrar:

- ferramentas utilizadas e em quais partes foram utilizadas;
- dois prompts completos com as respectivas respostas;
- pelo menos um erro, imprecisão ou invenção detectado e posteriormente verificado por execução do código;
- uma reflexão sobre a diferença entre aprender a partir da execução do código e receber uma resposta textual de um assistente.

---

# 7. Resumo dos resultados

| Experimento | Resultado |
|---|---|
| BFS | custo 49; 22 passos |
| DFS | custo 123; 48 passos |
| UCS | custo 40; 22 passos |
| A* h1 | custo 40; 120 expansões |
| A* h2 | custo 40; 115 expansões |
| A* h3 | custo 40; 27 expansões |
| Subida de encosta | média 34,6; DP 5,50; melhor 45 |
| Têmpera simulada | média 60,0; DP 0; melhor 60 |
| Pioras aceitas | 1043 em 30 execuções |
| PPV | 29,37% |
| Falsos a cada 100 positivos | 70,63 |
| Falsos positivos/semana | 23,70 |
| Tempo semanal com falsos | 4,74 h |
| PPV com sensibilidade de 99,9% | 29,99% |
| Maior grade testada | 800×800 |
| Falha até 800×800 | nenhuma |

---

# 8. Limitações

1. Os resultados numéricos dependem da semente definida pela matrícula utilizada.
2. 800×800 foi o maior tamanho efetivamente testado; o experimento não determina o limite absoluto da máquina.
3. h3 é utilizada para estudar o comportamento de uma heurística não admissível e não possui garantia geral de optimalidade.
4. O cálculo de dois testes positivos depende de hipóteses estatísticas adicionais.
5. Os tempos de execução dependem do computador e do ambiente Python utilizados.
6. O sistema especialista representa uma base de regras construída especificamente para o cenário da atividade.
7. Os parâmetros do sensor são gerados pelo mecanismo definido no projeto e representam o cenário experimental da atividade.

---

# 9. Estrutura do projeto

```text
caatinga-ai-sprint1/
├── README.md
├── RELATORIO.md
├── ANEXO_IA.md
├── requirements.txt
├── src/
│   ├── gerador_pomar.py
│   ├── buscas.py
│   ├── busca_local.py
│   ├── especialista.py
│   ├── bayes.py
│   ├── auditoria.py
│   ├── escalabilidade.py
│   ├── experimentos.py
│   └── main.py
└── resultados/
    ├── resultados.csv
    ├── resultados_busca_local.csv
    ├── grafico.png
    └── pomar.txt
```

O arquivo `gerador_pomar.py` deve permanecer inalterado, conforme especificação da atividade.

---

# 10. Conclusão

Os experimentos demonstraram que a variação dos custos dos talhões altera a escolha da estratégia de busca. BFS encontrou uma rota com o mesmo número de passos que UCS, mas com custo maior, enquanto UCS encontrou o menor custo na instância analisada.

O A* com Manhattan encontrou o mesmo custo da UCS e reduziu as expansões. A heurística 4×Manhattan reduziu ainda mais as expansões nesta execução, mas apresentou um contraexemplo de superestimação e, portanto, não possui a mesma garantia teórica.

Na busca local, a têmpera simulada apresentou aceitações de piora nas 30 execuções, evidenciando experimentalmente seu mecanismo de exploração.

No sistema especialista, a adição da R7 corrigiu uma lacuna identificada experimentalmente na base de regras, permitindo a cadeia R7 → R2 → R6.

Na análise probabilística, o PPV foi de 29,37%, mostrando que sensibilidade não deve ser interpretada como probabilidade de um alerta positivo ser verdadeiro. A análise também permitiu verificar quantitativamente as afirmações do laudo do fornecedor.
