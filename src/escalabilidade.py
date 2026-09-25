"""Experimento de escalabilidade das buscas do Caatinga.AI."""

import time

from gerador_pomar import gerar_pomar
from buscas import (
    busca_custo_uniforme,
    busca_a_estrela,
    heuristica_manhattan,
)


def executar_escalabilidade(matricula):
    """Executa UCS e A* Manhattan em diferentes tamanhos de pomar."""

    tamanhos = [12, 40, 100, 200, 400, 800]

    resultados = []

    print("\n=== ESCALABILIDADE ===")

    for n in tamanhos:
        print(f"\nTestando pomar {n}x{n}...")

        pomar = gerar_pomar(matricula, n=n)
        inicio = (0, 0)
        objetivo = (n - 1, n - 1)

        # -------------------------
        # UCS
        # -------------------------
        inicio_tempo = time.perf_counter()

        ucs = busca_custo_uniforme(
            pomar,
            inicio,
            objetivo,
        )

        tempo_ucs = (time.perf_counter() - inicio_tempo) * 1000

        # -------------------------
        # A* Manhattan
        # -------------------------
        inicio_tempo = time.perf_counter()

        astar = busca_a_estrela(
            pomar,
            inicio,
            objetivo,
            heuristica_manhattan,
            reabrir=True,
        )

        tempo_astar = (time.perf_counter() - inicio_tempo) * 1000

        resultado = {
            "tamanho": n,

            "ucs_custo": ucs["custo"],
            "ucs_passos": ucs["passos"],
            "ucs_expandidos": ucs["nos_expandidos"],
            "ucs_fronteira_max": ucs["fronteira_max"],
            "ucs_tempo_ms": tempo_ucs,

            "astar_custo": astar["custo"],
            "astar_passos": astar["passos"],
            "astar_expandidos": astar["nos_expandidos"],
            "astar_fronteira_max": astar["fronteira_max"],
            "astar_tempo_ms": tempo_astar,
        }

        resultados.append(resultado)

        print(
            f"UCS  | custo={ucs['custo']} | "
            f"expandidos={ucs['nos_expandidos']} | "
            f"fronteira={ucs['fronteira_max']} | "
            f"{tempo_ucs:.3f} ms"
        )

        print(
            f"A*   | custo={astar['custo']} | "
            f"expandidos={astar['nos_expandidos']} | "
            f"fronteira={astar['fronteira_max']} | "
            f"{tempo_astar:.3f} ms"
        )

    return resultados