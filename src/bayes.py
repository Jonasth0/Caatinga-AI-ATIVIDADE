"""Cálculos de Bayes para os parâmetros do sensor do Caatinga.AI."""


def calcular_bayes(prevalencia, sensibilidade, taxa_falso_positivo,
                   talhoes_por_semana, minutos_por_inspecao=12,
                   nova_sensibilidade=0.999):
    """Calcula PPV, falsos positivos e o cenário de nova sensibilidade."""
    p_positivo = (
        sensibilidade * prevalencia
        + taxa_falso_positivo * (1 - prevalencia)
    )
    ppv = sensibilidade * prevalencia / p_positivo
    falsos_semana = talhoes_por_semana * (1 - prevalencia) * taxa_falso_positivo
    horas_semana = falsos_semana * minutos_por_inspecao / 60

    novo_p_positivo = (
        nova_sensibilidade * prevalencia
        + taxa_falso_positivo * (1 - prevalencia)
    )
    novo_ppv = nova_sensibilidade * prevalencia / novo_p_positivo

    return {
        "p_positivo": p_positivo,
        "ppv": ppv,
        "falsos_a_cada_100": (1 - ppv) * 100,
        "falsos_por_semana": falsos_semana,
        "minutos_por_semana": falsos_semana * minutos_por_inspecao,
        "horas_por_semana": horas_semana,
        "nova_sensibilidade": nova_sensibilidade,
        "novo_ppv": novo_ppv,
        "novo_falsos_a_cada_100": (1 - novo_ppv) * 100,
    }


def imprimir_relatorio(parametros):
    """Exibe as contas de Bayes com os números da matrícula."""
    dados = calcular_bayes(**parametros)
    p = parametros["prevalencia"]
    s = parametros["sensibilidade"]
    f = parametros["taxa_falso_positivo"]
    n = parametros["talhoes_por_semana"]

    print("====================================")
    print("PARTE 4.3 - BAYES")
    print("====================================")
    print(f"Prevalência: {p:.4f}")
    print(f"Sensibilidade: {s:.4f}")
    print(f"Taxa de falso positivo: {f:.4f}")
    print(f"Talhões por semana: {n}")
    print()
    print("P(I|+) = (P(+|I) × P(I)) / "
          "(P(+|I)P(I) + P(+|não I)P(não I))")
    print(
        f"P(I|+) = ({s:.4f} × {p:.4f}) / "
        f"[({s:.4f} × {p:.4f}) + ({f:.4f} × {1-p:.4f})]"
    )
    print(f"P(infestado | positivo): {dados['ppv'] * 100:.2f}%")
    print(f"Falsos a cada 100 alertas: {dados['falsos_a_cada_100']:.2f}")
    print(f"Falsos por semana: {dados['falsos_por_semana']:.2f}")
    print(f"Horas por semana: {dados['horas_por_semana']:.2f}")
    print()
    print("Com sensibilidade de 99,9%:")
    print(f"Novo PPV: {dados['novo_ppv'] * 100:.2f}%")
    print(f"Novos falsos a cada 100: {dados['novo_falsos_a_cada_100']:.2f}")
    return dados


if __name__ == "__main__":
    from gerador_pomar import parametros_sensor
    import sys

    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 20231045
    imprimir_relatorio(parametros_sensor(matricula))
