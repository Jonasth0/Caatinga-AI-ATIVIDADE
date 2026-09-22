"""Estruturas iniciais para os algoritmos de busca do Caatinga.AI."""

from collections import deque

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
