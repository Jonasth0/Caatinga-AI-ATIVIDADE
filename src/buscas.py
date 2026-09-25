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

import heapq

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