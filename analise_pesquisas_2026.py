# Análise de amostragem das pesquisas eleitorais para presidente (Brasil, 2026)
# Pode ser executado no Google Colab: basta colar em uma célula e rodar.
import os
import numpy as np
import matplotlib.pyplot as plt

OUT = "graficos"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)

# Paleta (validada para daltonismo nas posições 1 e 2) e tinta neutra
FLAVIO, LULA = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "figure.dpi": 100, "savefig.dpi": 200, "savefig.bbox": "tight",
})
Z = 1.96  # nível de confiança de 95%

def moe(n, p=0.5, deff=1.0):
    """Margem de erro (pontos percentuais) de uma proporção."""
    return 100 * Z * np.sqrt(deff * p * (1 - p) / n)

# ---------------------------------------------------------------- dados
# Resultado oficial (TSE), % dos votos válidos
TSE_1T = {"Lula": 45.16, "Flávio": 47.03}
TSE_2T = {"Lula": 51.79, "Flávio": 48.21}
# Pesquisas de véspera, % dos votos válidos: (instituto, n, margem declarada, Lula, Flávio)
P1 = [("Datafolha\n3/10, n=4.006", 4006, 2.0, 45.0, 42.0),
      ("Quaest\n2–3/10, n=3.702", 3702, 2.0, 46.0, 45.0),
      ("AtlasIntel\n27/9–2/10, n=5.000", 5000, 1.0, 47.0, 44.1),
      ("CNT/MDA\n30/9–2/10, n=2.007", 2007, 2.2, 47.8, 42.1)]
P2 = [("Datafolha\n23–24/10, n=4.050", 4050, 2.0, 49.0, 51.0),
      ("Quaest\n23–24/10, n=3.702", 3702, 2.0, 49.0, 51.0),
      ("AtlasIntel\n24/10", None, None, 49.2, 50.8),
      ("CNT/MDA\nout/2026", None, None, 49.3, 50.7)]

# ------------------------------------------- Figura 1: margem de erro × n
n = np.linspace(400, 6000, 400)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(n, moe(n), color=INK, lw=2, label="Amostra aleatória simples (deff = 1)")
ax.plot(n, moe(n, deff=1.67), color=MUTED, lw=2, ls="--",
        label="Plano por conglomerados (deff ≈ 1,67)")
pts = [("Datafolha (1º e 2º turnos)", 4006, 2.0), ("Datafolha 2º t.", 4050, 2.0),
       ("Quaest", 3702, 2.0), ("AtlasIntel", 5000, 1.0), ("CNT/MDA", 2007, 2.2)]
for lab, nn, m in pts:
    ax.plot(nn, m, "o", ms=8, color=FLAVIO, mec="white", mew=1.5, zorder=3)
offs = {"Datafolha (1º e 2º turnos)": (-40, 12), "Datafolha 2º t.": None, "Quaest": (-50, -18),
        "AtlasIntel": (-30, -18), "CNT/MDA": (8, 6)}
for lab, nn, m in pts:
    if offs[lab] is None:
        continue
    ax.annotate(lab, (nn, m), xytext=offs[lab], textcoords="offset points", fontsize=8.5, color=INK)
ax.set_xlabel("Tamanho da amostra (n)")
ax.set_ylabel("Margem de erro (± pontos percentuais)")
ax.set_ylim(0, 6)
ax.legend(frameon=False, loc="upper right")
ax.set_title("Margem de erro para p = 50% com 95% de confiança", loc="left", fontsize=11, color=INK)
fig.savefig(f"{OUT}/fig1_margem_erro.png"); plt.close(fig)

# ------------------------------------- Figuras 2 e 3: pesquisas × urna
def pesquisa_vs_urna(dados, tse, titulo, arq, xlim, legloc="lower right"):
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    y = np.arange(len(dados))[::-1]
    for yi, (lab, nn, m, lula, flavio) in zip(y, dados):
        for val, cor, dy in ((flavio, FLAVIO, 0.12), (lula, LULA, -0.12)):
            ax.errorbar(val, yi + dy, xerr=m if m else None, fmt="o", ms=8, color=cor,
                        mec="white", mew=1.5, capsize=3, elinewidth=1.6)
    ax.axvline(tse["Flávio"], color=FLAVIO, lw=1.5, ls="--")
    ax.axvline(tse["Lula"], color=LULA, lw=1.5, ls="--")
    ax.text(tse["Flávio"], len(dados) - 0.35, f"Urna Flávio\n{tse['Flávio']:.2f}%".replace(".", ","),
            color=INK, fontsize=8.5, ha="center", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.text(tse["Lula"], len(dados) - 0.35, f"Urna Lula\n{tse['Lula']:.2f}%".replace(".", ","),
            color=INK, fontsize=8.5, ha="center", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.set_yticks(y, [d[0] for d in dados], fontsize=8.5)
    ax.set_xlim(*xlim); ax.set_ylim(-0.6, len(dados) + 0.4)
    ax.set_xlabel("% dos votos válidos (barras = margem de erro declarada)")
    ax.plot([], [], "o", color=FLAVIO, label="Flávio Bolsonaro (PL)")
    ax.plot([], [], "o", color=LULA, label="Lula (PT)")
    ax.legend(frameon=True, facecolor="white", edgecolor="white", loc=legloc, fontsize=8.5)
    ax.set_title(titulo, loc="left", fontsize=11, color=INK)
    ax.grid(axis="y", visible=False)
    fig.savefig(f"{OUT}/{arq}"); plt.close(fig)

pesquisa_vs_urna(P1, TSE_1T, "1º turno: pesquisas de véspera × resultado oficial", "fig2_primeiro_turno.png", (38, 52), legloc="upper left")
pesquisa_vs_urna(P2, TSE_2T, "2º turno: pesquisas de véspera × resultado oficial", "fig3_segundo_turno.png", (45, 55))

# --------------------------------- Figura 4: série do Datafolha (1º turno)
datas = ["1–2/9", "8–11/9", "15–16/9", "22–24/9", "28/9–1/10", "3/10"]
lula_s = [38, 39, 39, 40, 42, 42]
flav_s = [33, 35, 36, 36, 38, 40]
fig, ax = plt.subplots(figsize=(7.2, 3.8))
x = np.arange(len(datas))
ax.plot(x, lula_s, "-o", color=LULA, lw=2, ms=7, mec="white", mew=1.5, label="Lula (PT)")
ax.plot(x, flav_s, "-o", color=FLAVIO, lw=2, ms=7, mec="white", mew=1.5, label="Flávio Bolsonaro (PL)")
for xi, a, b in zip(x, lula_s, flav_s):
    ax.text(xi, a + 0.6, f"{a}", ha="center", fontsize=8.5, color=INK)
    ax.text(xi, b - 1.4, f"{b}", ha="center", fontsize=8.5, color=INK)
ax.set_xticks(x, datas)
ax.set_ylim(28, 46)
ax.set_ylabel("% do total de entrevistados")
ax.set_xlabel("Período de campo (2026)")
ax.legend(frameon=False, loc="upper left")
ax.set_title("Datafolha, 1º turno (estimulada, votos totais): a diferença caiu de 5 para 2 pontos",
             loc="left", fontsize=10.5, color=INK)
fig.savefig(f"{OUT}/fig4_serie_datafolha.png"); plt.close(fig)

# ----------------------- Figura 5: espontânea do 2º turno (Datafolha × Quaest)
cats = ["Flávio Bolsonaro", "Lula", "Outras respostas", "Branco/nulo/não vota", "Indecisos"]
cores = [FLAVIO, LULA, "#b8b6ae", "#8d8b84", "#d9d7d0"]
dados5 = {"Datafolha\n23–24/10": [47, 45, 1, 3, 4], "Quaest\n23–24/10": [44, 42, 0, 7, 7]}
fig, ax = plt.subplots(figsize=(7.2, 2.8))
for i, (lab, vals) in enumerate(dados5.items()):
    left = 0
    for v, c, cat in zip(vals, cores, cats):
        if v == 0:
            continue
        ax.barh(i, v, left=left, color=c, edgecolor="white", linewidth=2, height=0.6,
                label=cat if i == 0 or cat == "Outras respostas" else None)
        if v >= 4:
            ax.text(left + v / 2, i, f"{v}%", ha="center", va="center", fontsize=9,
                    color="white" if c in (FLAVIO, LULA, "#8d8b84") else INK)
        left += v
ax.set_yticks([0, 1], list(dados5.keys()))
ax.invert_yaxis(); ax.set_xlim(0, 100); ax.grid(False)
ax.set_xlabel("% do total de entrevistados")
h, l = ax.get_legend_handles_labels()
uniq = dict(zip(l, h))
ax.legend([uniq[c] for c in cats if c in uniq], [c for c in cats if c in uniq],
          frameon=False, ncol=3, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.32))
ax.set_title("2º turno, pergunta espontânea (sem lista de nomes)", loc="left", fontsize=11, color=INK)
fig.savefig(f"{OUT}/fig5_espontanea.png"); plt.close(fig)

# --------------- Figura 6: simulação do erro amostral (Datafolha, 1º turno)
p_real = TSE_1T["Flávio"] / 100
n_val = round(4006 * 0.93)  # descontando 4% brancos/nulos e 3% indecisos
sims = 10_000
aas = rng.binomial(n_val, p_real, sims) / n_val * 100
# Conglomerados: inflaciona a variância pelo efeito do plano (deff = 1,67)
cong = rng.normal(p_real * 100, np.sqrt(1.67) * aas.std(), sims)
fig, ax = plt.subplots(figsize=(7.2, 3.8))
bins = np.arange(40, 54.01, 0.5)
ax.hist(cong, bins=bins, color="#b8b6ae", edgecolor="white", linewidth=0.6, label="Conglomerados (deff ≈ 1,67)")
ax.hist(aas, bins=bins, color=FLAVIO, alpha=0.85, edgecolor="white", linewidth=0.6, label="Amostra aleatória simples")
ax.axvline(42, color=INK, lw=2)
ax.annotate("Datafolha publicou 42%", (42, ax.get_ylim()[1] * 0.8), xytext=(6, 0),
            textcoords="offset points", fontsize=9, color=INK)
ax.axvline(p_real * 100, color=INK, lw=1.2, ls="--")
ax.annotate("Urna: 47,03%", (p_real * 100, ax.get_ylim()[1] * 0.95), xytext=(-80, 0),
            textcoords="offset points", fontsize=9, color=INK)
ax.set_xlabel("% de Flávio Bolsonaro nos votos válidos em cada amostra simulada")
ax.set_ylabel("Nº de amostras")
ax.legend(frameon=False, loc="upper right", fontsize=8.5)
ax.grid(axis="x", visible=False)
ax.set_title(f"10.000 amostras simuladas de n = {n_val:,} votos válidos".replace(",", "."),
             loc="left", fontsize=11, color=INK)
fig.savefig(f"{OUT}/fig6_simulacao.png"); plt.close(fig)

# ---------------------------------------------------------- números-chave
print("n0 (e=2pp, p=0,5):", Z**2 * 0.25 / 0.02**2)
N = 158_745_079
n0 = Z**2 * 0.25 / 0.02**2
print("n com correção finita:", n0 / (1 + (n0 - 1) / N))
for lab, nn, m in pts:
    print(f"{lab}: AAS = ±{moe(nn):.2f} pp | declarada ±{m} | deff implícito = {(m / moe(nn))**2:.2f}")
print("n válidos Datafolha 1T:", n_val, "| margem AAS p=0,47:", round(moe(n_val, p_real), 2))
print("Prob. AAS <= 42%:", (aas <= 42).mean(), "| conglomerados:", (cong <= 42).mean())
print("Erro em erros-padrão (AAS):", round((47.03 - 42) / aas.std(), 1),
      "| (deff 1,67):", round((47.03 - 42) / (np.sqrt(1.67) * aas.std()), 1))
for nome, d, t in (("1T", P1, TSE_1T), ("2T", P2, TSE_2T)):
    for lab, nn, m, lula, flavio in d:
        print(nome, lab.split("\n")[0], "erro Flávio:", round(flavio - t["Flávio"], 2),
              "erro Lula:", round(lula - t["Lula"], 2), "margem:", m)
