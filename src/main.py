"""Ponto de entrada: gera o pomar e executa os experimentos do Sprint 1."""

import csv
import sys
from pathlib import Path

from gerador_pomar import gerar_pomar, parametros_sensor
from buscas import executar_todas_buscas
from busca_local import executar_30
from bayes import calcular_bayes
from especialista import imprimir_prova


def salvar_pomar(pomar, matricula, destino):
    """Salva a semente na primeira linha e a grade nas linhas seguintes."""
    with destino.open("w", encoding="utf-8") as arquivo:
        arquivo.write(f"matricula-semente: {matricula}\n")
        for linha in pomar:
            arquivo.write(" ".join(linha) + "\n")


def salvar_resultados(resultados, destino):
    """Gera o CSV no formato exigido pelo enunciado."""
    campos = [
        "estrategia", "heuristica", "custo", "passos",
        "nos_expandidos", "fronteira_max", "tempo_ms"
    ]
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for resultado in resultados:
            escritor.writerow({
                campo: resultado[campo] for campo in campos
            })


def salvar_resultados_locais(dados, destino):
    """Salva as 30 execuções das buscas locais para facilitar o relatório."""
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "rodada", "subida_encosta", "tempera_simulada", "pioras_aceitas"
        ])
        escritor.writerows(dados["detalhes"])


def gerar_grafico(resultados, destino):
    """Cria o gráfico obrigatório de nós expandidos por estratégia."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rotulos = [
        f"{r['estrategia']} {r['heuristica']}".strip()
        for r in resultados
    ]
    valores = [r["nos_expandidos"] for r in resultados]

    plt.figure(figsize=(10, 5))
    plt.bar(rotulos, valores)
    plt.ylabel("Nós expandidos")
    plt.xlabel("Estratégia")
    plt.title("Caatinga.AI — Nós expandidos por estratégia")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(destino, dpi=150)
    plt.close()


def imprimir_resumo(matricula, resultados, locais, bayes):
    """Mostra no terminal os números principais para conferência."""
    print("\n=== RESULTADOS DAS BUSCAS ===")
    for r in resultados:
        print(
            f"{r['estrategia']:3} {r['heuristica']:18} | "
            f"custo={r['custo']:3} | passos={r['passos']:3} | "
            f"expandidos={r['nos_expandidos']:4} | "
            f"fronteira_max={r['fronteira_max']:3} | "
            f"{r['tempo_ms']:.3f} ms"
        )

    print("\n=== BUSCA LOCAL — 30 EXECUÇÕES ===")
    print("Subida:", locais["subida"])
    print("Têmpera:", locais["tempera"])
    print("Pioras aceitas:", locais["pioras_aceitas_total"])

    print("\n=== BAYES ===")
    print(f"PPV: {bayes['ppv'] * 100:.2f}%")
    print(f"Falsos por semana: {bayes['falsos_por_semana']:.2f}")
    print(f"Horas por semana: {bayes['horas_por_semana']:.2f}")
    print(f"PPV com sensibilidade 99,9%: {bayes['novo_ppv'] * 100:.2f}%")
    print(f"\nSemente utilizada: {matricula}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python src/main.py <matricula>")
        return 1

    matricula = int(sys.argv[1])
    raiz = Path(__file__).resolve().parents[1]
    resultados_dir = raiz / "resultados"
    resultados_dir.mkdir(exist_ok=True)

    # A matrícula define tanto o pomar quanto os parâmetros do sensor.
    pomar = gerar_pomar(matricula)
    sensor = parametros_sensor(matricula)
    inicio = (0, 0)
    objetivo = (len(pomar) - 1, len(pomar[0]) - 1)

    # Executa BFS, DFS, UCS e A* com as três heurísticas.
    resultados = executar_todas_buscas(pomar, inicio, objetivo)

    # Executa os métodos de busca local 30 vezes, como pede a atividade.
    locais = executar_30(pomar, matricula)

    # Calcula Bayes diretamente a partir da semente, sem números fixos.
    bayes = calcular_bayes(**sensor)

    salvar_pomar(pomar, matricula, resultados_dir / "pomar.txt")
    salvar_resultados(resultados, resultados_dir / "resultados.csv")
    salvar_resultados_locais(locais, resultados_dir / "resultados_busca_local.csv")
    gerar_grafico(resultados, resultados_dir / "grafico.png")

    # Exibe o sistema especialista para documentar o encadeamento.
    fatos = {
        "armadilha_positiva",
        "umidade_baixa",
        "dias_desde_pulverizacao_maior_14",
    }
    print("\n=== SISTEMA ESPECIALISTA ===")
    imprimir_prova("manejo_urgente", fatos)

    imprimir_resumo(matricula, resultados, locais, bayes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
