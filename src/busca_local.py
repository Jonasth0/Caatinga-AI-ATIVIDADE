import random
import math


K = 15


def talhoes_livres(pomar):
    """Retorna todas as células que podem ser inspecionadas."""
    livres = []

    for linha in range(len(pomar)):
        for coluna in range(len(pomar[0])):
            if pomar[linha][coluna] != "#":
                livres.append((linha, coluna))

    return livres


def valor_talhao(pomar, estado):
    """Define a prioridade de um talhão."""
    linha, coluna = estado

    if pomar[linha][coluna] == "~":
        return 4

    return 1


def estado_inicial(pomar, semente=None):
    """Cria um estado inicial aleatório com K talhões."""
    livres = talhoes_livres(pomar)

    if semente is not None:
        random.seed(semente)

    return set(random.sample(livres, K))


def funcao_objetivo(pomar, estado):
    """Calcula o valor total dos talhões selecionados."""
    return sum(
        valor_talhao(pomar, talhao)
        for talhao in estado
    )


def gerar_vizinho(pomar, estado, livres):
    """Gera um vizinho trocando um talhão selecionado."""

    novo_estado = set(estado)

    selecionado = random.choice(
        list(novo_estado)
    )

    disponiveis = [
        talhao
        for talhao in livres
        if talhao not in novo_estado
    ]

    novo_talhao = random.choice(
        disponiveis
    )

    novo_estado.remove(
        selecionado
    )

    novo_estado.add(
        novo_talhao
    )

    return novo_estado


def subida_de_encosta(pomar, semente=None):
    """Executa a busca local por subida de encosta."""

    livres = talhoes_livres(pomar)

    estado_atual = estado_inicial(
        pomar,
        semente
    )

    valor_atual = funcao_objetivo(
        pomar,
        estado_atual
    )

    while True:

        vizinho = gerar_vizinho(
            pomar,
            estado_atual,
            livres
        )

        valor_vizinho = funcao_objetivo(
            pomar,
            vizinho
        )

        if valor_vizinho <= valor_atual:
            break

        estado_atual = vizinho
        valor_atual = valor_vizinho

    return estado_atual, valor_atual


def tempera_simulada(
    pomar,
    semente=None,
    temperatura_inicial=5.0,
    taxa_resfriamento=0.95,
    iteracoes=2000
):
    """Executa a busca local por têmpera simulada."""

    if semente is not None:
        random.seed(semente)

    livres = talhoes_livres(pomar)

    estado_atual = estado_inicial(
        pomar,
        semente
    )

    valor_atual = funcao_objetivo(
        pomar,
        estado_atual
    )

    melhor_estado = set(
        estado_atual
    )

    melhor_valor = valor_atual

    temperatura = temperatura_inicial

    pioras_aceitas = 0

    for _ in range(iteracoes):

        vizinho = gerar_vizinho(
            pomar,
            estado_atual,
            livres
        )

        valor_vizinho = funcao_objetivo(
            pomar,
            vizinho
        )

        diferenca = (
            valor_vizinho
            - valor_atual
        )

        if diferenca > 0:

            aceitar = True

        else:

            probabilidade = math.exp(
                diferenca / temperatura
            )

            aceitar = (
                random.random()
                < probabilidade
            )

            if aceitar:
                pioras_aceitas += 1

        if aceitar:

            estado_atual = vizinho
            valor_atual = valor_vizinho

        if valor_atual > melhor_valor:

            melhor_estado = set(
                estado_atual
            )

            melhor_valor = valor_atual

        temperatura *= taxa_resfriamento

        if temperatura < 0.001:
            temperatura = 0.001

    return (
        melhor_estado,
        melhor_valor,
        pioras_aceitas
    )


# TESTE DAS BUSCAS LOCAIS

if __name__ == "__main__":

    from gerador_pomar import gerar_pomar
    from statistics import mean, stdev

    pomar = gerar_pomar(20231045)

    resultados_subida = []
    resultados_tempera = []
    pioras_tempera = []
    resultados_detalhados = []

    # Executa cada algoritmo 30 vezes
    for rodada in range(30):

        semente = 20231045 + rodada

        # Subida de encosta
        _, valor_subida = subida_de_encosta(
            pomar,
            semente=semente
        )

        resultados_subida.append(
            valor_subida
        )

        # Têmpera simulada
        _, valor_tempera, pioras = tempera_simulada(
            pomar,
            semente=semente
        )

        resultados_tempera.append(
            valor_tempera
        )

        pioras_tempera.append(
            pioras
        )

        resultados_detalhados.append(
            (
                rodada + 1,
                valor_subida,
                valor_tempera,
                pioras
            )
        )
        
    # Resultados da subida de encosta

    print("====================================")
    print("SUBIDA DE ENCOSTA - 30 EXECUÇÕES")
    print("====================================")

    print(
        "Resultados:",
        resultados_subida
    )

    print(
        "Média:",
        mean(resultados_subida)
    )

    print(
        "Desvio padrão:",
        stdev(resultados_subida)
    )

    print(
        "Melhor valor:",
        max(resultados_subida)
    )

    # Resultados da têmpera simulada

    print()
    print("====================================")
    print("TÊMPERA SIMULADA - 30 EXECUÇÕES")
    print("====================================")

    print(
        "Resultados:",
        resultados_tempera
    )

    print(
        "Média:",
        mean(resultados_tempera)
    )

    print(
        "Desvio padrão:",
        stdev(resultados_tempera)
    )

    print(
        "Melhor valor:",
        max(resultados_tempera)
    )

    print(
        "Pioras aceitas em cada execução:",
        pioras_tempera
    )

    print(
        "Total de pioras aceitas:",
        sum(pioras_tempera)
    )

    print()
    print("====================================")
    print("RESULTADOS DAS 30 EXECUÇÕES")
    print("====================================")

    print(
        "Rodada | Subida | Têmpera | Pioras aceitas"
    )

    for rodada, subida, tempera, pioras in resultados_detalhados:
        print(
            f"{rodada:6} | "
            f"{subida:7} | "
            f"{tempera:7} | "
            f"{pioras:15}"
        )