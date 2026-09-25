# Caatinga.AI — Sprint 1

Projeto da disciplina de Inteligência Artificial.

## 1. Estado atual

Nesta etapa foram implementadas as principais funcionalidades previstas para o
Sprint 1, incluindo estratégias de busca, busca local, sistema especialista,
análise probabilística e auditoria das afirmações do sistema.

## 1.1 Execução

```bash
python src/main.py 24114049
```

## 1.2 Estrutura do projeto

```text
src/
├── gerador_pomar.py
├── buscas.py
├── busca_local.py
├── especialista.py
├── bayes.py
└── main.py
```

---

# 2. Busca não informada

## 2.1 BFS

Foi implementada a Busca em Largura (BFS), utilizando uma fila para controlar
a fronteira de busca.

## 2.2 DFS

Foi implementada a Busca em Profundidade (DFS), utilizando uma pilha para
controlar a fronteira.

A BFS foi mantida para permitir a comparação entre as duas estratégias.

## 2.3 UCS

Foi implementada a Busca de Custo Uniforme (UCS), considerando os diferentes
custos de entrada das células do pomar.

Células normais possuem custo 1 e células de terreno difícil (`~`) possuem
custo 4.

---

# 3. Busca informada

## 3.1 A*

Foi implementado o algoritmo A* com três heurísticas:

- `h1(n) = 0`;
- `h2(n) = Manhattan`;
- `h3(n) = 4 × Manhattan`.

Para a semente `20231045`, foram obtidos:

| Estratégia | Custo | Nós expandidos |
|---|---:|---:|
| UCS | 34 | 112 |
| A* h1 | 34 | 112 |
| A* h2 | 34 | 93 |
| A* h3 | 34 | 25 |

## 3.2 Admissibilidade

A heurística Manhattan é admissível porque representa um limite inferior do
custo restante.

A heurística `4 × Manhattan` não é admissível, pois pode superestimar o custo
real. No exemplo analisado, para o estado `(11,10)` e objetivo `(11,11)`, o
valor da heurística é 4, enquanto o custo real restante é 1.

## 3.3 Comparação com UCS

A UCS e o A* com `h3` encontraram custo 34 nessa execução.

Entretanto, o A* com `h3` expandiu apenas 25 nós contra 112 da UCS, uma redução
de aproximadamente 77,7%.

A igualdade dos custos nessa execução não comprova a admissibilidade de `h3`.

## 3.4 Busca local

Foi implementada a seleção de `K = 15` talhões utilizando:

- Subida de encosta (Hill Climbing);
- Têmpera simulada (Simulated Annealing).

Foram realizadas 30 execuções de cada método, registrando média, desvio
padrão, melhor resultado e resultados individuais.

A função de valor considera:

```text
. = 1
~ = 4
```

O valor máximo possível para 15 talhões é 60.

---

# 4. Raciocínio e incerteza

## 4.1 Sistema especialista

Foi implementado um sistema especialista utilizando regras de produção e
encadeamento para trás (backward chaining).

A base possui 8 regras relacionadas a:

- armadilhas;
- umidade;
- risco de infestação;
- prioridade de inspeção;
- manejo;
- autorização de aplicação.

## 4.2 Correção da base de regras

Durante os testes foi identificada uma situação em que uma armadilha positiva
com umidade baixa não permitia concluir risco de infestação.

A falha foi corrigida com a criação da regra R7, permitindo que o sistema
completasse o encadeamento nesse cenário.

## 4.3 Análise de Bayes

Os parâmetros utilizados foram:

```text
Prevalência: 0,0337
Sensibilidade: 0,99
Falso positivo: 0,03
Talhões por semana: 1200
```

O valor calculado para a probabilidade de um alerta positivo representar
infestação real foi de aproximadamente **53,51%**.

Foram estimados aproximadamente **34,79 falsos alertas por semana**, equivalentes
a cerca de **6,96 horas semanais** de inspeção.

Também foi analisado o aumento da sensibilidade para 99,9%, mantendo a taxa de
falso positivo em 3%. Nesse cenário, o valor preditivo positivo passou para
aproximadamente **53,73%**.

## 4.4 Regra explícita

Foi adicionada uma regra para impedir uma nova aplicação quando o intervalo
mínimo entre aplicações não tiver sido atingido.

Essa decisão permanece como regra explícita para facilitar a explicação,
auditoria e responsabilização pelas decisões do sistema.

---

# 5. Auditoria das afirmações

## 5.1 Afirmação sobre A*

A afirmação de que o A* com `4 × Manhattan` sempre entrega a rota mais barata
foi considerada **incorreta**, pois essa heurística não é admissível.

## 5.2 Afirmação sobre BFS e A*

A afirmação de redução de aproximadamente 38% no custo foi considerada
**parcialmente correta**.

No experimento:

```text
BFS = 55
A* Manhattan = 34
```

A redução foi de aproximadamente 38,18%.

## 5.3 Afirmação sobre sensibilidade

A afirmação de que 99% dos alertas positivos representam infestações foi
considerada **incorreta**.

A sensibilidade mede a capacidade de detectar casos realmente infestados, não a
probabilidade de um resultado positivo ser verdadeiro.

O valor calculado foi de aproximadamente 53,51%.

## 5.4 Afirmação sobre dois testes positivos

A afirmação de que dois resultados positivos garantem confiança superior a 99%
foi considerada **incorreta**.

Considerando independência condicional entre os testes, o valor calculado foi
de aproximadamente 97,45%.

## 5.5 Afirmação sobre DFS

A afirmação foi considerada **parcialmente correta**.

A DFS pode utilizar menos memória em determinados espaços de busca, mas isso
não significa que ela sempre encontre a rota de menor custo.

---

# 6. Resultado final

O Sprint 1 reúne diferentes técnicas de Inteligência Artificial aplicadas ao
cenário do Caatinga.AI, incluindo buscas não informadas e informadas, métodos
de busca local, sistema especialista, encadeamento de regras e análise
probabilística.

Os experimentos também permitiram identificar limitações das heurísticas,
interpretar corretamente métricas de sensores e avaliar criticamente as
afirmações feitas sobre o sistema.