"""Estruturas iniciais para os algoritmos de busca do Caatinga.AI."""

from collections import deque
import heapq

ORDEM = [
    (-1, 0),  # norte
    (1, 0),   # sul
    (0, -1),  # oeste
    (0, 1),   # leste
]


def vizinhos(pomar, estado):
    """Retorna os estados vizinhos que podem ser visitados."""
    linha, coluna = estado
    resultado = []

    for dl, dc in ORDEM:
        nl, nc = linha + dl, coluna + dc

        if 0 <= nl < len(pomar) and 0 <= nc < len(pomar[0]):
            if pomar[nl][nc] != "#":
                resultado.append((nl, nc))

    return resultado

def custo_entrada(pomar, estado):
    """Retorna o custo de entrar em uma célula."""
    return 4 if pomar[estado[0]][estado[1]] == "~" else 1

def custo_caminho(pomar, caminho):
    """Calcula o custo total de um caminho."""
    custo = 0

    for estado in caminho[1:]:
        custo += custo_entrada(pomar, estado)

    return custo


def reconstruir(pai, inicio, objetivo):
    """Reconstrói o caminho usando o dicionário de pais."""
    caminho = []
    atual = objetivo

    while atual is not None:
        caminho.append(atual)
        if atual == inicio:
            break
        atual = pai[atual]

    caminho.reverse()
    return caminho


def busca_largura(pomar, inicio, objetivo):
    """Busca em largura (BFS).

    Nesta primeira versão, a função já encontra um caminho, mas as métricas
    detalhadas do trabalho ainda serão acrescentadas posteriormente.
    """
    fila = deque([inicio])
    visitados = {inicio}
    pai = {inicio: None}

    while fila:
        atual = fila.popleft()

        if atual == objetivo:
            return reconstruir(pai, inicio, objetivo)

        for vizinho in vizinhos(pomar, atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pai[vizinho] = atual
                fila.append(vizinho)

    return []


def busca_profundidade(pomar, inicio, objetivo):
    """Busca em profundidade (DFS) usando uma pilha."""
    pilha = [inicio]
    visitados = {inicio}
    pai = {inicio: None}

    while pilha:
        atual = pilha.pop()

        if atual == objetivo:
            return reconstruir(pai, inicio, objetivo)

        # A pilha é LIFO. Inserimos os vizinhos em ordem inversa
        # para que a próxima expansão respeite ORDEM.
        for vizinho in reversed(vizinhos(pomar, atual)):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pai[vizinho] = atual
                pilha.append(vizinho)

    return []


# Próximas etapas do projeto:
# - busca de custo uniforme (UCS)
# - A* e heurísticas

def busca_custo_uniforme(pomar, inicio, objetivo):
    """Busca de custo uniforme (UCS)."""

    fila = []
    contador = 0

    heapq.heappush(fila, (0, contador, inicio))

    melhor_custo = {inicio: 0}
    pai = {inicio: None}

    while fila:
        custo_atual, _, atual = heapq.heappop(fila)

        if custo_atual != melhor_custo.get(atual):
            continue

        if atual == objetivo:
            return reconstruir(pai, inicio, objetivo)

        for vizinho in vizinhos(pomar, atual):

            novo_custo = (
                custo_atual
                + custo_entrada(pomar, vizinho)
            )

            if novo_custo < melhor_custo.get(
                vizinho,
                float("inf")
            ):
                melhor_custo[vizinho] = novo_custo
                pai[vizinho] = atual

                contador += 1

                heapq.heappush(
                    fila,
                    (
                        novo_custo,
                        contador,
                        vizinho
                    )
                )

    return []

#adição de novas funções!

def heuristica_zero(estado, objetivo):
    """h1(n) = 0."""
    return 0


def heuristica_manhattan(estado, objetivo):
    """h2(n) = distância de Manhattan até o objetivo."""
    linha, coluna = estado
    linha_obj, coluna_obj = objetivo

    return abs(linha - linha_obj) + abs(coluna - coluna_obj)


def heuristica_manhattan_4(estado, objetivo):
    """h3(n) = 4 × distância de Manhattan até o objetivo."""
    return 4 * heuristica_manhattan(estado, objetivo)

def busca_a_estrela(pomar, inicio, objetivo, heuristica):
    """Busca A* usando a heurística recebida."""

    fila = []

    contador = 0
    expandidos = 0

    custo_g = {
        inicio: 0
    }

    pai = {
        inicio: None
    }

    f_inicial = heuristica(
        inicio,
        objetivo
    )

    heapq.heappush(
        fila,
        (
            f_inicial,
            0,
            contador,
            inicio
        )
    )

    while fila:

        f_atual, g_atual, _, atual = heapq.heappop(fila)

        # Ignora uma entrada antiga da fila.
        if g_atual != custo_g.get(atual):
            continue

        expandidos += 1

        if atual == objetivo:
            caminho = reconstruir(
                pai,
                inicio,
                objetivo
            )

            custo = custo_caminho(
                pomar,
                caminho
            )

            return caminho, custo, expandidos

        for vizinho in vizinhos(
            pomar,
            atual
        ):

            custo_movimento = custo_entrada(
                pomar,
                vizinho
            )

            novo_g = (
                g_atual
                + custo_movimento
            )

            if novo_g < custo_g.get(
                vizinho,
                float("inf")
            ):

                custo_g[vizinho] = novo_g

                pai[vizinho] = atual

                h = heuristica(
                    vizinho,
                    objetivo
                )

                f = novo_g + h

                contador += 1

                heapq.heappush(
                    fila,
                    (
                        f,
                        novo_g,
                        contador,
                        vizinho
                    )
                )

    return [], 0, expandidos

#Admissibilidade parte 3.2 concluida!
#breve relatorio sobre a situação
#A heurística h2(n), baseada na distância de Manhattan, é admissível porque cada movimento altera apenas uma coordenada em uma unidade e o menor custo de entrada em uma célula é 1. Dessa forma, a
#distância de Manhattan nunca supera o custo real mínimo necessário para alcançar o objetivo. Já a heurística h3(n) = 4 × Manhattan não é admissível. No pomar gerado pela matrícula 20231045,
#considerando a célula (11,10) e o objetivo (11,11), a distância de Manhattan é 1 e h3 = 4. Entretanto, a célula objetivo possui custo de entrada 1, fazendo com que o custo real restante seja 1. Como 4 > 1, h3 superestima o custo real.
#Continuação da proxima fase!