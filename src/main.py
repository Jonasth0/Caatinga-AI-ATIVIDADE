"""Ponto de entrada da primeira versão do Caatinga.AI."""

import sys

from gerador_pomar import gerar_pomar
from buscas import busca_largura, busca_profundidade


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

    print("Caatinga.AI - Sprint 1")
    print(f"Matrícula: {matricula}")
    print(f"Tamanho do pomar: {len(pomar)}x{len(pomar[0])}")
    print(f"Caminho encontrado pela BFS: {caminho_bfs}")
    print(f"Caminho encontrado pela DFS: {caminho_dfs}")


if __name__ == "__main__":
    main()
