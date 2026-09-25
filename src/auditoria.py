"""Cálculos de apoio para a Parte 5 — auditoria do laudo do fornecedor."""


def auditoria(resultados, bayes):
    """Compara as afirmações do laudo com os resultados medidos."""
    por_nome = {(r["estrategia"], r["heuristica"]): r for r in resultados}
    ucs = por_nome[("UCS", "")]
    bfs = por_nome[("BFS", "")]
    a_h2 = por_nome[("A*", "h2 = Manhattan")]
    a_h3 = por_nome[("A*", "h3 = 4 × Manhattan")]

    reducao_bfs_astar = (bfs["custo"] - a_h2["custo"]) / bfs["custo"] * 100
    p = bayes["ppv"]
    # Sob independência condicional, dois positivos têm atualização quadrática.
    sens = 0.99
    prev = None  # A prevalência não precisa ser duplicada aqui; vem do PPV abaixo.
    # A fórmula geral é aplicada pelo chamador quando houver parâmetros do sensor.

    print("=== AUDITORIA DO LAUDO ===")
    print("1. A* com h3 sempre ótimo: incorreta se h3 for não admissível.")
    print(
        f"   Medido: UCS={ucs['custo']} e A* h3={a_h3['custo']} "
        f"(nesta execução)."
    )
    print(
        f"2. Redução BFS -> A* Manhattan: {reducao_bfs_astar:.2f}% "
        f"(custo BFS={bfs['custo']}, A*={a_h2['custo']})."
    )
    print(
        f"3. Sensibilidade não é PPV. PPV medido/calculado: {p * 100:.2f}%."
    )
    print(
        "4. Dois positivos não podem ser avaliados apenas pela sensibilidade; "
        "é necessário considerar prevalência, especificidade e independência."
    )
    print(
        "5. DFS pode economizar memória, mas não garante menor custo; "
        "a própria comparação DFS/UCS fornece a evidência."
    )


if __name__ == "__main__":
    print("Execute a auditoria pelo main.py para usar os resultados da sua semente.")
