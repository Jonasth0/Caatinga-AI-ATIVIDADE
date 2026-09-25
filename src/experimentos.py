"""Experimentos adicionais exigidos pelo enunciado, especialmente 2.4."""

import time

from gerador_pomar import gerar_pomar
from buscas import (
    busca_largura,
    busca_profundidade,
    busca_custo_uniforme,
    busca_a_estrela,
    heuristica_manhattan,
)

# Sequência progressiva pedida no enunciado. Pode parar quando um limite for atingido.
TAMANHOS_PADRAO = [12, 40, 100, 200, 400, 800]


def estados_teoricos(n):
    """No modelo de grade, existem no máximo n² estados de posição."""
    return n * n


def executar_escalabilidade(
    semente,
    tamanhos=TAMANHOS_PADRAO,
    limite_segundos=60.0,
):
    """Mede cada estratégia até uma execução superar o limite de 60 s."""
    estrategias = [
        ("BFS", busca_largura, None),
        ("DFS", busca_profundidade, None),
        ("UCS", busca_custo_uniforme, None),
        ("A* Manhattan", busca_a_estrela, heuristica_manhattan),
    ]
    linhas = []
    falha = None

    for n in tamanhos:
        pomar = gerar_pomar(semente, n)
        inicio = (0, 0)
        objetivo = (n - 1, n - 1)
        for nome, funcao, heuristica in estrategias:
            inicio_t = time.perf_counter()
            try:
                if heuristica is None:
                    resultado = funcao(pomar, inicio, objetivo)
                else:
                    resultado = funcao(
                        pomar, inicio, objetivo, heuristica, reabrir=True
                    )
                duracao = time.perf_counter() - inicio_t
                atingiu_limite = duracao > limite_segundos
                linhas.append({
                    "n": n,
                    "estrategia": nome,
                    "status": "falhou_tempo" if atingiu_limite else "ok",
                    "tempo_s": duracao,
                    "custo": resultado["custo"],
                    "passos": resultado["passos"],
                    "nos_expandidos": resultado["nos_expandidos"],
                    "fronteira_max": resultado["fronteira_max"],
                    "estados_teoricos_n2": estados_teoricos(n),
                })
                if atingiu_limite and falha is None:
                    falha = {
                        "n": n,
                        "estrategia": nome,
                        "tipo": "tempo > 60 s",
                        "tempo_s": duracao,
                        "limite_teorico": (
                            "O espaço de estados da grade contém no máximo n² posições; "
                            "neste ponto a limitação prática observada foi o tempo."
                        ),
                    }
                    return linhas, falha
            except (MemoryError, RecursionError) as exc:
                duracao = time.perf_counter() - inicio_t
                tipo = type(exc).__name__
                linhas.append({
                    "n": n,
                    "estrategia": nome,
                    "status": "falhou_" + tipo.lower(),
                    "tempo_s": duracao,
                    "custo": "",
                    "passos": "",
                    "nos_expandidos": "",
                    "fronteira_max": "",
                    "estados_teoricos_n2": estados_teoricos(n),
                })
                falha = {
                    "n": n,
                    "estrategia": nome,
                    "tipo": tipo,
                    "tempo_s": duracao,
                    "limite_teorico": (
                        "O espaço de estados da grade tem no máximo n² posições."
                    ),
                }
                return linhas, falha

    return linhas, falha
