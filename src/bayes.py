# src/bayes.py

# ==========================================
# PARÂMETROS DO SENSOR
# ==========================================

prevalencia = 0.0337
sensibilidade = 0.99
taxa_falso_positivo = 0.03
talhoes_por_semana = 1200

# ==========================================
# 4.3(a) - VALOR PREDITIVO POSITIVO
# ==========================================

# P(infestado | sensor positivo)
#
# P(I|+) = P(+|I) * P(I)
#         -------------------------------
#         P(+|I)P(I) + P(+|não I)P(não I)

probabilidade_positivo = (
    sensibilidade * prevalencia
    + taxa_falso_positivo * (1 - prevalencia)
)

ppv = (
    sensibilidade * prevalencia
    / probabilidade_positivo
)

# ==========================================
# 4.3(b) - FALSOS ALERTAS A CADA 100
# ==========================================

percentual_falsos_alertas = (1 - ppv) * 100

# ==========================================
# 4.3(c) - FALSOS ALERTAS POR SEMANA
# ==========================================

falsos_por_semana = (
    talhoes_por_semana
    * (1 - prevalencia)
    * taxa_falso_positivo
)

# Cada inspeção custa 12 minutos
minutos_por_inspecao = 12

minutos_semana = falsos_por_semana * minutos_por_inspecao

horas_semana = minutos_semana / 60

# ==========================================
# 4.3(d) - SENSIBILIDADE DE 99,9%
# ==========================================

nova_sensibilidade = 0.999

novo_probabilidade_positivo = (
    nova_sensibilidade * prevalencia
    + taxa_falso_positivo * (1 - prevalencia)
)

novo_ppv = (
    nova_sensibilidade * prevalencia
    / novo_probabilidade_positivo
)

novo_percentual_falsos = (1 - novo_ppv) * 100

# ==========================================
# RESULTADOS
# ==========================================

print("====================================")
print("PARTE 4.3 - BAYES")
print("====================================")

print()
print("PARÂMETROS:")
print(f"Prevalência: {prevalencia:.4f}")
print(f"Sensibilidade: {sensibilidade:.4f}")
print(f"Taxa de falso positivo: {taxa_falso_positivo:.4f}")
print(f"Talhões por semana: {talhoes_por_semana}")

# ------------------------------------------
# 4.3(a)
# ------------------------------------------

print()
print("====================================")
print("4.3(a) - P(INFESTADO | POSITIVO)")
print("====================================")

print("Fórmula:")
print(
    "P(I|+) = [P(+|I) × P(I)] / "
    "[P(+|I) × P(I) + P(+|não I) × P(não I)]"
)

print()
print("Substituição:")
print(
    f"P(I|+) = ({sensibilidade:.4f} × {prevalencia:.4f}) / "
    f"[({sensibilidade:.4f} × {prevalencia:.4f}) + "
    f"({taxa_falso_positivo:.4f} × {1 - prevalencia:.4f})]"
)

print()
print(f"P(+) = {probabilidade_positivo:.6f}")
print(f"P(infestado | positivo) = {ppv:.6f}")
print(f"Percentual = {ppv * 100:.2f}%")

# ------------------------------------------
# 4.3(b)
# ------------------------------------------

print()
print("====================================")
print("4.3(b) - FALSOS ALERTAS")
print("====================================")

print(
    f"A cada 100 alertas do sistema, "
    f"cerca de {percentual_falsos_alertas:.1f} serão falsos."
)

# ------------------------------------------
# 4.3(c)
# ------------------------------------------

print()
print("====================================")
print("4.3(c) - IMPACTO SEMANAL")
print("====================================")

print(
    f"Falsos alertas por semana: "
    f"{falsos_por_semana:.2f}"
)

print(
    f"Minutos gastos por semana: "
    f"{minutos_semana:.2f}"
)

print(
    f"Horas gastas por semana: "
    f"{horas_semana:.2f}"
)

# ------------------------------------------
# 4.3(d)
# ------------------------------------------

print()
print("====================================")
print("4.3(d) - SENSIBILIDADE DE 99,9%")
print("====================================")

print(f"Nova sensibilidade: {nova_sensibilidade:.4f}")

print(
    f"Novo P(infestado | positivo): "
    f"{novo_ppv:.6f}"
)

print(
    f"Novo percentual de positivos verdadeiros: "
    f"{novo_ppv * 100:.2f}%"
)

print(
    f"Novo percentual de falsos alertas: "
    f"{novo_percentual_falsos:.2f}%"
)

print()
print("COMPARAÇÃO:")
print(f"PPV original: {ppv * 100:.2f}%")
print(f"PPV com sensibilidade de 99,9%: {novo_ppv * 100:.2f}%")
print(
    f"Variação do PPV: "
    f"{(novo_ppv - ppv) * 100:.2f} pontos percentuais"
)

print()
print("INTERPRETAÇÃO:")
print(
    "A alteração da sensibilidade para 99,9% "
    "aumenta o valor preditivo positivo apenas "
    "ligeiramente quando a taxa de falsos positivos "
    "permanece em 3%."
)

print(
    "Para reduzir de forma mais significativa os "
    "alertas falsos, o parâmetro diretamente relacionado "
    "a esse problema é a taxa de falso positivo."
)