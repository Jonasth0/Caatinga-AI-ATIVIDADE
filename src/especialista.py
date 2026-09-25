"""Mini sistema especialista do Caatinga.AI com backward chaining."""

REGRAS = [
    {"nome": "R1", "se": ["armadilha_positiva", "umidade_alta"],
     "entao": "risco_infestacao"},
    {"nome": "R2", "se": ["risco_infestacao", "dias_desde_pulverizacao_maior_14"],
     "entao": "inspecionar_prioridade_alta"},
    {"nome": "R3", "se": ["armadilha_positiva", "umidade_baixa",
                            "nao_ha_risco_adicional"],
     "entao": "inspecionar_prioridade_media"},
    # Regra criada para corrigir o caso legítimo da Parte 4.2.
    {"nome": "R7", "se": ["armadilha_positiva", "umidade_baixa",
                           "dias_desde_pulverizacao_maior_14"],
     "entao": "risco_infestacao"},
    # Decisão de segurança permanece explícita e auditável.
    {"nome": "R8", "se": ["intervalo_minimo_aplicacao_nao_atingido"],
     "entao": "nao_autorizar_aplicacao"},
    {"nome": "R4", "se": ["armadilha_negativa"],
     "entao": "inspecionar_prioridade_baixa"},
    {"nome": "R5", "se": ["risco_infestacao", "talhao_encharcado"],
     "entao": "inspecionar_prioridade_alta"},
    {"nome": "R6", "se": ["inspecionar_prioridade_alta"],
     "entao": "manejo_urgente"},
]


def provar(objetivo, fatos, regras=REGRAS, visitados=None, nivel=0, trace=None):
    """Tenta provar o objetivo e guarda o traço de regras usado."""
    if visitados is None:
        visitados = set()
    if trace is None:
        trace = []

    indentacao = "  " * nivel
    if objetivo in fatos:
        trace.append(f"{indentacao}FATO: {objetivo}")
        return True, trace

    if objetivo in visitados:
        trace.append(f"{indentacao}CICLO EVITADO: {objetivo}")
        return False, trace

    visitados.add(objetivo)

    for regra in regras:
        if regra["entao"] != objetivo:
            continue

        trace.append(
            f"{indentacao}Tentando {regra['nome']}: "
            f"SE {' E '.join(regra['se'])} ENTÃO {regra['entao']}"
        )

        sucesso = True
        for condicao in regra["se"]:
            sucesso, trace = provar(
                condicao, fatos, regras, visitados, nivel + 1, trace
            )
            if not sucesso:
                break

        if sucesso:
            trace.append(f"{indentacao}✓ {regra['nome']} sustentou {objetivo}")
            return True, trace

    trace.append(f"{indentacao}✗ Não foi possível provar {objetivo}")
    return False, trace


def imprimir_prova(objetivo, fatos, regras=REGRAS):
    """Imprime a cadeia de explicação para auditoria."""
    resultado, trace = provar(objetivo, fatos, regras)
    for linha in trace:
        print(linha)
    print(f"\nConclusão: {'SIM' if resultado else 'NÃO'} — {objetivo}")
    return resultado, trace


def regras_com_correcao():
    """Retorna uma cópia da base sem R7 para reproduzir o erro da Parte 4.2."""
    return [regra for regra in REGRAS if regra["nome"] != "R7"]


if __name__ == "__main__":
    fatos = {
        "armadilha_positiva",
        "umidade_baixa",
        "dias_desde_pulverizacao_maior_14",
    }
    print("=== ANTES DA CORREÇÃO (sem R7) ===")
    imprimir_prova("manejo_urgente", fatos, regras_com_correcao())
    print("\n=== DEPOIS DA CORREÇÃO ===")
    imprimir_prova("manejo_urgente", fatos)
