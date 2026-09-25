"""Busca local para selecionar K talhões de maior prioridade."""

import math
import random
from statistics import mean, stdev

K = 15


def talhoes_livres(pomar):
    """Lista os talhões que não estão bloqueados."""
    return [
        (linha, coluna)
        for linha in range(len(pomar))
        for coluna in range(len(pomar[0]))
        if pomar[linha][coluna] != "#"
    ]


def valor_talhao(pomar, estado):
    """Usa o custo do terreno como valor de prioridade do talhão."""
    return 4 if pomar[estado[0]][estado[1]] == "~" else 1


def estado_inicial(pomar, rng=None):
    """Gera uma solução aleatória com exatamente K talhões."""
    rng = rng or random
    livres = talhoes_livres(pomar)
    if len(livres) < K:
        raise ValueError("O pomar possui menos de K talhões livres.")
    return set(rng.sample(livres, K))


def funcao_objetivo(pomar, estado):
    """Soma a prioridade dos K talhões escolhidos."""
    return sum(valor_talhao(pomar, talhao) for talhao in estado)


def gerar_vizinho(pomar, estado, livres, rng=None):
    """Troca um talhão escolhido por outro que ainda não foi escolhido."""
    rng = rng or random
    novo_estado = set(estado)
    removido = rng.choice(tuple(novo_estado))
    disponiveis = [t for t in livres if t not in novo_estado]
    adicionado = rng.choice(disponiveis)
    novo_estado.remove(removido)
    novo_estado.add(adicionado)
    return novo_estado


def subida_de_encosta(pomar, semente=None):
    """Aceita apenas vizinhos estritamente melhores."""
    rng = random.Random(semente)
    livres = talhoes_livres(pomar)
    estado_atual = estado_inicial(pomar, rng)
    valor_atual = funcao_objetivo(pomar, estado_atual)

    while True:
        vizinho = gerar_vizinho(pomar, estado_atual, livres, rng)
        valor_vizinho = funcao_objetivo(pomar, vizinho)
        if valor_vizinho <= valor_atual:
            break
        estado_atual, valor_atual = vizinho, valor_vizinho

    return estado_atual, valor_atual


def tempera_simulada(
    pomar,
    semente=None,
    temperatura_inicial=5.0,
    taxa_resfriamento=0.995,
    temperatura_minima=0.001,
    iteracoes=2000,
):
    """Aceita algumas pioras para escapar de ótimos locais."""
    rng = random.Random(semente)
    livres = talhoes_livres(pomar)
    estado_atual = estado_inicial(pomar, rng)
    valor_atual = funcao_objetivo(pomar, estado_atual)
    melhor_estado = set(estado_atual)
    melhor_valor = valor_atual
    temperatura = temperatura_inicial
    pioras_aceitas = 0

    for _ in range(iteracoes):
        vizinho = gerar_vizinho(pomar, estado_atual, livres, rng)
        valor_vizinho = funcao_objetivo(pomar, vizinho)
        diferenca = valor_vizinho - valor_atual

        # Melhoras sempre entram; pioras entram com probabilidade de Boltzmann.
        if diferenca >= 0:
            aceitar = True
        else:
            probabilidade = math.exp(diferenca / temperatura)
            aceitar = rng.random() < probabilidade
            if aceitar:
                pioras_aceitas += 1

        if aceitar:
            estado_atual, valor_atual = vizinho, valor_vizinho

        if valor_atual > melhor_valor:
            melhor_estado = set(estado_atual)
            melhor_valor = valor_atual

        temperatura = max(temperatura * taxa_resfriamento, temperatura_minima)

    return melhor_estado, melhor_valor, pioras_aceitas


def executar_30(pomar, semente_base):
    """Executa os dois métodos 30 vezes e calcula as estatísticas pedidas."""
    subidas = []
    temperas = []
    pioras = []
    detalhes = []

    for rodada in range(30):
        semente = semente_base + rodada
        _, valor_subida = subida_de_encosta(pomar, semente)
        _, valor_tempera, qtd_pioras = tempera_simulada(pomar, semente)
        subidas.append(valor_subida)
        temperas.append(valor_tempera)
        pioras.append(qtd_pioras)
        detalhes.append((rodada + 1, valor_subida, valor_tempera, qtd_pioras))

    def estatisticas(valores):
        return {
            "media": mean(valores),
            "desvio_padrao": stdev(valores) if len(valores) > 1 else 0.0,
            "melhor": max(valores),
        }

    return {
        "subida": estatisticas(subidas),
        "tempera": estatisticas(temperas),
        "pioras_aceitas_total": sum(pioras),
        "detalhes": detalhes,
    }


if __name__ == "__main__":
    from gerador_pomar import gerar_pomar
    import sys

    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 20231045
    dados = executar_30(gerar_pomar(matricula), matricula)
    print("Subida:", dados["subida"])
    print("Têmpera:", dados["tempera"])
    print("Pioras aceitas:", dados["pioras_aceitas_total"])
