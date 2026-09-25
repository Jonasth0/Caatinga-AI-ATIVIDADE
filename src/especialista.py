# src/especialista.py


# ==========================================
# BASE DE REGRAS
# ==========================================

REGRAS = [
    {
        "nome": "R1",
        "se": ["armadilha_positiva", "umidade_alta"],
        "entao": "risco_infestacao"
    },
    {
        "nome": "R2",
        "se": ["risco_infestacao", "dias_desde_pulverizacao_maior_14"],
        "entao": "inspecionar_prioridade_alta"
    },
#Caso problemático:
#Com armadilha_positiva, umidade_baixa e dias_desde_pulverizacao_maior_14, a regra R3 inicialmente
#classificava o talhão apenas como inspecionar_prioridade_media. A base não conseguia reconhecer o risco
#de infestação nesse cenário porque a R1 exigia umidade_alta.
    {
        "nome": "R3",
        "se": [
        "armadilha_positiva",
        "umidade_baixa",
        "nao_ha_risco_adicional"
    ],
        "entao": "inspecionar_prioridade_media"
    },
#Correção:
#SE armadilha_positiva E umidade_baixa E dias_desde_pulverizacao_maior_14 ENTÃO risco_infestacao.
#Com a correção, o encadeamento para trás conseguiu provar risco_infestacao pela R7 e, em seguida,
#tilizar a R2 para chegar a inspecionar_prioridade_alta, permitindo que a R6 concluísse manejo_urgente.
    {
        "nome": "R7",
        "se": [
           "armadilha_positiva",
           "umidade_baixa",
           "dias_desde_pulverizacao_maior_14"
    ],
        "entao": "risco_infestacao"
    },
#R8 Adição da parte 4.4:
#decisão que deve permanecer como regra explícita é a não autorização de uma nova aplicação quando o intervalo mínimo estabelecido não tiver sido cumprido.
#Essa decisão deve ser auditável, pois o responsável precisa conseguir verificar diretamente qual condição levou ao bloqueio. Dessa forma, a decisão não depende de uma justificativa implícita de um modelo
#aprendido, permitindo identificar claramente o fato observado, a regra aplicada e o responsável pela decisão.
    {
    "nome": "R8",
    "se": ["intervalo_minimo_aplicacao_nao_atingido"],
    "entao": "nao_autorizar_aplicacao"
    },

    {
        "nome": "R4",
        "se": ["armadilha_negativa"],
        "entao": "inspecionar_prioridade_baixa"
    },
    {
        "nome": "R5",
        "se": ["risco_infestacao", "talhao_encharcado"],
        "entao": "inspecionar_prioridade_alta"
    },
    {
        "nome": "R6",
        "se": ["inspecionar_prioridade_alta"],
        "entao": "manejo_urgente"
    }
]


# ==========================================
# ENCADEAMENTO PARA TRÁS
# ==========================================

def provar(objetivo, fatos, regras, visitados=None, nivel=0):
    """
    Tenta provar um objetivo usando encadeamento para trás.
    Retorna True ou False e imprime o caminho das regras.
    """

    if visitados is None:
        visitados = set()

    indentacao = "  " * nivel

    # O fato já é conhecido
    if objetivo in fatos:
        print(
            f"{indentacao}FATO: {objetivo}"
        )
        return True

    # Evita ciclos
    if objetivo in visitados:
        return False

    visitados.add(objetivo)

    # Procura regras que possam gerar o objetivo
    for regra in regras:

        if regra["entao"] != objetivo:
            continue

        print(
            f"{indentacao}Tentando {regra['nome']}: "
            f"SE {' E '.join(regra['se'])} "
            f"ENTÃO {regra['entao']}"
        )

        todas_condicoes = True

        for condicao in regra["se"]:

            if not provar(
                condicao,
                fatos,
                regras,
                visitados,
                nivel + 1
            ):
                todas_condicoes = False
                break

        if todas_condicoes:
            print(
                f"{indentacao}✓ {regra['nome']} sustentou "
                f"{objetivo}"
            )

            return True

    return False


# ==========================================
# TESTES
# ==========================================

# ==========================================
# TESTE DA PARTE 4.2
# ==========================================

if __name__ == "__main__":

    fatos = {
        "armadilha_positiva",
        "umidade_baixa",
        "dias_desde_pulverizacao_maior_14"
    }

    objetivo = "manejo_urgente"

    print("====================================")
    print("PARTE 4.2 - BASE CORRIGIDA")
    print("====================================")

    print("Fatos observados:")
    for fato in sorted(fatos):
        print("-", fato)

    print()
    print("Objetivo:", objetivo)
    print()
    print("TRAÇO DO ENCADEAMENTO:")
    print()

    resultado = provar(
        objetivo,
        fatos,
        REGRAS
    )

    print()

    if resultado:
        print("Conclusão:", objetivo)
    else:
        print("Não foi possível provar:", objetivo)