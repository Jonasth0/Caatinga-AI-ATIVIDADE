"""Ponto de entrada da primeira versão do Caatinga.AI."""

import sys

from gerador_pomar import gerar_pomar
from buscas import (
    busca_largura,
    busca_profundidade,
    busca_custo_uniforme,
    busca_a_estrela,
    heuristica_zero,
    heuristica_manhattan,
    heuristica_manhattan_4,
)


def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <matricula>")
        return

    matricula = int(sys.argv[1])
    pomar = gerar_pomar(matricula)

    inicio = (0, 0)
    objetivo = (len(pomar) - 1, len(pomar[0]) - 1)

    caminho_bfs = busca_largura(pomar, inicio, objetivo)
    caminho_dfs = busca_profundidade(pomar, inicio, objetivo)

    caminho_ucs = busca_custo_uniforme(
        pomar,
        inicio,
        objetivo
    )

    caminho_a_h1, custo_h1, expandidos_h1 = busca_a_estrela(
        pomar,
        inicio,
        objetivo,
        heuristica_zero
    )

    caminho_a_h2, custo_h2, expandidos_h2 = busca_a_estrela(
        pomar,
        inicio,
        objetivo,
        heuristica_manhattan
    )

    caminho_a_h3, custo_h3, expandidos_h3 = busca_a_estrela(
        pomar,
        inicio,
        objetivo,
        heuristica_manhattan_4
    )

    print("Caatinga.AI - Sprint 1")
    print(f"Matrícula: {matricula}")
    print(f"Tamanho do pomar: {len(pomar)}x{len(pomar[0])}")
    print(f"Caminho encontrado pela BFS: {caminho_bfs}")
    print(f"Caminho encontrado pela DFS: {caminho_dfs}")
    print(f"Caminho encontrado pela UCS: {caminho_ucs}")
    print(f"Nós expandidos pelo A* h1 = 0: {expandidos_h1}")
    print(f"Nós expandidos pelo A* h2 = Manhattan: {expandidos_h2}")
    print(f"Nós expandidos pelo A* h3 = 4 × Manhattan: {expandidos_h3}")
    print(f"Custo da rota A* h1 = 0: {custo_h1}")
    print(f"Custo da rota A* h2 = Manhattan: {custo_h2}")
    print(f"Custo da rota A* h3 = 4 × Manhattan: {custo_h3}")  

if __name__ == "__main__":
    main()