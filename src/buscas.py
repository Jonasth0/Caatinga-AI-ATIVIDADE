"""Algoritmos de busca usados pelo Caatinga.AI."""

from collections import deque
import heapq
import time

# A ordem é fixa para tornar BFS/DFS/A* reproduzíveis.
ORDEM = [
    (-1, 0),  # Norte
    (1, 0),   # Sul
    (0, -1),  # Oeste
    (0, 1),   # Leste
]


def vizinhos(pomar, estado):
    """Retorna vizinhos livres na ordem declarada no relatório."""
    linha, coluna = estado
    resultado = []
    for dl, dc in ORDEM:
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < len(pomar) and 0 <= nc < len(pomar[0]):
            if pomar[nl][nc] != "#":
                resultado.append((nl, nc))
    return resultado


def custo_entrada(pomar, estado):
    """Calcula o custo de entrar no talhão."""
    return 4 if pomar[estado[0]][estado[1]] == "~" else 1


def custo_caminho(pomar, caminho):
    """Soma os custos dos estados depois do estado inicial."""
    return sum(custo_entrada(pomar, estado) for estado in caminho[1:])


def reconstruir(pai, inicio, objetivo):
    """Reconstrói a rota a partir do mapa de predecessores."""
    caminho = []
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        if atual == inicio:
            break
        atual = pai[atual]
    caminho.reverse()
    return caminho if caminho and caminho[0] == inicio else []


def _resultado(caminho, custo, expandidos, fronteira_max, inicio, tempo_ms):
    """Centraliza as métricas usadas por todas as buscas."""
    return {
        "caminho": caminho,
        "custo": custo,
        "passos": max(0, len(caminho) - 1),
        "nos_expandidos": expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": tempo_ms,
    }


def busca_largura(pomar, inicio, objetivo):
    """Busca em largura: minimiza o número de passos, não o custo."""
    inicio_t = time.perf_counter()
    fila = deque([inicio])
    visitados = {inicio}
    pai = {inicio: None}
    expandidos = 0
    fronteira_max = len(fila)

    while fila:
        atual = fila.popleft()
        if atual == objetivo:
            caminho = reconstruir(pai, inicio, objetivo)
            return _resultado(
                caminho, custo_caminho(pomar, caminho), expandidos,
                fronteira_max, inicio, (time.perf_counter() - inicio_t) * 1000
            )

        expandidos += 1
        for vizinho in vizinhos(pomar, atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pai[vizinho] = atual
                fila.append(vizinho)
        fronteira_max = max(fronteira_max, len(fila))

    return _resultado([], 0, expandidos, fronteira_max, inicio,
                      (time.perf_counter() - inicio_t) * 1000)


def busca_profundidade(pomar, inicio, objetivo):
    """Busca em profundidade usando pilha e a ORDEM declarada."""
    inicio_t = time.perf_counter()
    pilha = [inicio]
    visitados = {inicio}
    pai = {inicio: None}
    expandidos = 0
    fronteira_max = len(pilha)

    while pilha:
        atual = pilha.pop()
        if atual == objetivo:
            caminho = reconstruir(pai, inicio, objetivo)
            return _resultado(
                caminho, custo_caminho(pomar, caminho), expandidos,
                fronteira_max, inicio, (time.perf_counter() - inicio_t) * 1000
            )

        expandidos += 1
        # A inversão preserva a ordem lógica quando a pilha é LIFO.
        for vizinho in reversed(vizinhos(pomar, atual)):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pai[vizinho] = atual
                pilha.append(vizinho)
        fronteira_max = max(fronteira_max, len(pilha))

    return _resultado([], 0, expandidos, fronteira_max, inicio,
                      (time.perf_counter() - inicio_t) * 1000)


def busca_custo_uniforme(pomar, inicio, objetivo):
    """UCS: sempre expande o menor custo acumulado conhecido."""
    inicio_t = time.perf_counter()
    fila = []
    contador = 0
    heapq.heappush(fila, (0, contador, inicio))
    melhor_custo = {inicio: 0}
    pai = {inicio: None}
    expandidos = 0
    fronteira_max = len(fila)

    while fila:
        custo_atual, _, atual = heapq.heappop(fila)
        if custo_atual != melhor_custo.get(atual):
            continue

        if atual == objetivo:
            caminho = reconstruir(pai, inicio, objetivo)
            return _resultado(
                caminho, custo_atual, expandidos, fronteira_max,
                inicio, (time.perf_counter() - inicio_t) * 1000
            )

        expandidos += 1
        for vizinho in vizinhos(pomar, atual):
            novo_custo = custo_atual + custo_entrada(pomar, vizinho)
            if novo_custo < melhor_custo.get(vizinho, float("inf")):
                melhor_custo[vizinho] = novo_custo
                pai[vizinho] = atual
                contador += 1
                heapq.heappush(fila, (novo_custo, contador, vizinho))
        fronteira_max = max(fronteira_max, len(fila))

    return _resultado([], 0, expandidos, fronteira_max, inicio,
                      (time.perf_counter() - inicio_t) * 1000)


def heuristica_zero(estado, objetivo):
    """h1(n) = 0; transforma A* em UCS."""
    return 0


def heuristica_manhattan(estado, objetivo):
    """h2(n): distância de Manhattan."""
    return abs(estado[0] - objetivo[0]) + abs(estado[1] - objetivo[1])


def heuristica_manhattan_4(estado, objetivo):
    """h3(n): 4 vezes a distância de Manhattan."""
    return 4 * heuristica_manhattan(estado, objetivo)


def busca_a_estrela(pomar, inicio, objetivo, heuristica, reabrir=True):
    """A* com reabertura opcional de estados quando surge um g menor."""
    inicio_t = time.perf_counter()
    fila = []
    contador = 0
    custo_g = {inicio: 0}
    pai = {inicio: None}
    # O conjunto fechado é usado somente quando a reabertura é desativada.
    fechados = set()
    expandidos = 0
    fronteira_max = 1
    heapq.heappush(fila, (heuristica(inicio, objetivo), 0, contador, inicio))

    while fila:
        f_atual, g_atual, _, atual = heapq.heappop(fila)
        if g_atual != custo_g.get(atual):
            continue
        if not reabrir and atual in fechados:
            continue

        if atual == objetivo:
            caminho = reconstruir(pai, inicio, objetivo)
            return _resultado(
                caminho, g_atual, expandidos, fronteira_max,
                inicio, (time.perf_counter() - inicio_t) * 1000
            )

        expandidos += 1
        if not reabrir:
            fechados.add(atual)

        for vizinho in vizinhos(pomar, atual):
            novo_g = g_atual + custo_entrada(pomar, vizinho)
            if novo_g >= custo_g.get(vizinho, float("inf")):
                continue
            if not reabrir and vizinho in fechados:
                continue

            custo_g[vizinho] = novo_g
            pai[vizinho] = atual
            contador += 1
            f = novo_g + heuristica(vizinho, objetivo)
            heapq.heappush(fila, (f, novo_g, contador, vizinho))

        fronteira_max = max(fronteira_max, len(fila))

    return _resultado([], 0, expandidos, fronteira_max, inicio,
                      (time.perf_counter() - inicio_t) * 1000)


def executar_todas_buscas(pomar, inicio, objetivo):
    """Executa as estratégias exigidas e devolve uma lista tabular."""
    configuracoes = [
        ("BFS", "", busca_largura, None),
        ("DFS", "", busca_profundidade, None),
        ("UCS", "", busca_custo_uniforme, None),
        ("A*", "h1 = 0", busca_a_estrela, heuristica_zero),
        ("A*", "h2 = Manhattan", busca_a_estrela, heuristica_manhattan),
        ("A*", "h3 = 4 × Manhattan", busca_a_estrela, heuristica_manhattan_4),
    ]
    resultados = []
    for estrategia, heuristica_nome, funcao, heuristica in configuracoes:
        if heuristica is None:
            resultado = funcao(pomar, inicio, objetivo)
        else:
            resultado = funcao(pomar, inicio, objetivo, heuristica, reabrir=True)
        resultados.append({
            "estrategia": estrategia,
            "heuristica": heuristica_nome,
            **resultado,
        })
    return resultados
