# Caatinga.AI — Sprint 1

Implementação da Atividade Prática Avaliativa de Inteligência Artificial.

> **Importante:** `src/gerador_pomar.py` foi mantido exatamente como fornecido no enunciado.

## Execução

Recomendado: Python 3.10+.

```bash
pip install -r requirements.txt
python src/main.py <matricula>
```

Exemplo:

```bash
python src/main.py 20231045
```

O comando gera do zero:

```text
resultados/
├── resultados.csv
├── resultados_busca_local.csv
├── grafico.png
└── pomar.txt
```

## Organização

- `gerador_pomar.py` — gerador oficial do enunciado; não alterar.
- `buscas.py` — BFS, DFS, UCS e A*, com métricas de custo, passos, expansão e fronteira.
- `busca_local.py` — subida de encosta e têmpera simulada, com 30 execuções.
- `especialista.py` — regras e encadeamento para trás, incluindo o caso de correção da Parte 4.2.
- `bayes.py` — cálculos de Bayes usando os parâmetros da matrícula.
- `auditoria.py` — apoio à análise das afirmações do fornecedor.
- `main.py` — ponto de entrada que executa e salva os experimentos.

## Decisões de implementação

A ordem de expansão dos vizinhos é:

```text
Norte → Sul → Oeste → Leste
```

Ela é mantida em todas as estratégias para tornar os resultados reproduzíveis.

O A* utiliza reabertura de estados: se um caminho com custo `g` menor for encontrado,
o estado pode voltar à fronteira.

A fronteira máxima registrada é o maior tamanho atingido pela estrutura durante
a execução, e não o tamanho ao final.

## Métricas

O arquivo `resultados.csv` segue o formato exigido:

```text
estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms
```

Os resultados devem ser obtidos executando o código com a **matrícula da dupla**.
Não copie números de outra semente para o relatório.

## Busca local

Para `K = 15`, são feitas 30 execuções de cada método. O arquivo
`resultados_busca_local.csv` contém os resultados individuais e as estatísticas
são exibidas no terminal.

A função de objetivo usada nesta implementação é a soma dos valores dos talhões:

```text
. = 1
~ = 4
```

## Verificação

Antes da entrega, compare a implementação com a caixa de aferição do enunciado
usando a matrícula fictícia `20231045`. Os valores de custo e passos indicados
pelo professor devem bater exatamente; pequenas diferenças no número de nós
expandidos podem ocorrer conforme o critério de desempate da fila.

## Ainda precisa ser produzido manualmente

O código automatiza os experimentos, mas não substitui o relatório. Ainda é
necessário preencher `RELATORIO.md` com as respostas teóricas das Partes 1–5,
registrar a evidência dos experimentos e preparar `ANEXO_IA.md` com o uso real
de assistentes de IA.
