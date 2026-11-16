r"""Gera as figuras do README a partir das saídas salvas, sem treinar modelos.

Execute na raiz com: .\.venv\Scripts\python.exe docs\gerar_graficos.py
"""

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
NOTEBOOK = json.loads((ROOT / "projeto_final.ipynb").read_text(encoding="utf-8"))
EVIDENCE = NOTEBOOK["metadata"]["evidencias_bloco02"]
METRICS = {row["modelo"]: row for row in EVIDENCE["metricas"]}

distribution_cell = next(
    cell for cell in NOTEBOOK["cells"]
    if cell["cell_type"] == "code" and "distribuicao_alvo =" in "".join(cell["source"])
)
distribution_text = "\n".join(
    "".join(output.get("data", {}).get("text/plain", []))
    for output in distribution_cell["outputs"]
)
distribution = {
    int(label): (int(count), float(percent))
    for label, count, percent in re.findall(
        r"^\s*([01])\s+(\d+)\s+([\d.]+)\s*$", distribution_text, re.MULTILINE
    )
}
raw = ROOT / "data" / "raw" / "manutencao_preditiva.csv"
assert hashlib.sha256(raw.read_bytes()).hexdigest() == EVIDENCE["sha256_csv"]
with raw.open(encoding="utf-8-sig", newline="") as stream:
    counts = Counter(int(row["falha_maquina"]) for row in csv.DictReader(stream))
assert distribution == {0: (9661, 96.61), 1: (339, 3.39)}
assert counts == {label: values[0] for label, values in distribution.items()}
assert EVIDENCE["escolhas"] == {
    "KNN": {"modelo__n_neighbors": 5}, "Arvore": {"modelo__max_depth": 5}
}

NAVY = "#244764"
TEAL = "#167D8D"
ORANGE = "#C47520"
INK = "#172B3A"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 12,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": "#BCC9D2",
    "xtick.color": INK, "ytick.color": INK, "figure.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
})
ASSETS.mkdir(parents=True, exist_ok=True)


def percent(value):
    return f"{value:.2f}%".replace(".", ",")


def save(figure, filename, source):
    figure.text(0.03, 0.025, source, fontsize=9, color="#526674")
    figure.savefig(ASSETS / filename, dpi=200, facecolor="white")
    plt.close(figure)


fig, ax = plt.subplots(figsize=(10, 5.2))
fig.subplots_adjust(left=0.15, right=0.98, top=0.78, bottom=0.20)
fig.suptitle("Distribuição da base oficial", x=0.03, y=0.96, ha="left", fontsize=21, weight="bold")
fig.text(0.03, 0.87, "10.000 registros antes do balanceamento", fontsize=12)
bars = ax.barh(["Normal", "Falha"], [distribution[0][0], distribution[1][0]],
               color=[NAVY, ORANGE], height=0.48)
ax.invert_yaxis()
ax.set_xlim(0, 12600)
ax.set_xlabel("Quantidade de registros")
ax.set_axisbelow(True)
ax.grid(axis="x", color="#E3E9EE")
for bar, (count, share) in zip(bars, [distribution[0], distribution[1]]):
    number = f"{count:,}".replace(",", ".")
    ax.text(bar.get_width() + 170, bar.get_y() + bar.get_height() / 2,
            f"{number}  |  {percent(share)}", va="center", weight="bold")
save(fig, "distribuicao-classes.png", "Fonte: notebook, Fase 1. Contagens conferidas com o CSV oficial preservado.")

fig, ax = plt.subplots(figsize=(10, 5.8))
fig.subplots_adjust(left=0.09, right=0.98, top=0.73, bottom=0.17)
fig.suptitle("Comparativo dos modelos selecionados", x=0.03, y=0.96, ha="left", fontsize=21, weight="bold")
fig.text(0.03, 0.88, "Teste preservado: 2.000 registros, incluindo 68 falhas", fontsize=12)
keys = ["acuracia_teste", "precisao_falha", "recall_falha", "f1_falha"]
labels = ["Acurácia", "Precisão da falha", "Recall da falha", "F1 da falha"]
for offset, name, label, color in [
    (-0.19, "KNN", "KNN · K=5", NAVY),
    (0.19, "Arvore", "Árvore · profundidade=5", TEAL),
]:
    values = [METRICS[name][key] * 100 for key in keys]
    bars = ax.bar([index + offset for index in range(4)], values, width=0.34, color=color, label=label)
    ax.bar_label(bars, labels=[percent(value) for value in values], padding=5, fontsize=11)
ax.set_xticks(range(4), labels)
ax.set_ylim(0, 102)
ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
ax.set_ylabel("Resultado no teste (%)")
ax.set_axisbelow(True)
ax.grid(axis="y", color="#E3E9EE")
fig.legend(loc="upper left", bbox_to_anchor=(0.07, 0.84), ncol=2, frameon=False, fontsize=11)
save(fig, "comparativo-modelos.png", "Fonte: notebook, métricas finais do Bloco 02. Precisão, recall e F1 para a classe de falha.")

tree = METRICS["Arvore"]
assert [tree[key] for key in ["tn", "fp", "fn", "tp"]] == [1731, 201, 11, 57]
fig, ax = plt.subplots(figsize=(8.6, 6.5))
fig.subplots_adjust(left=0.20, right=0.92, top=0.78, bottom=0.18)
fig.suptitle("Onde a árvore acerta e erra", x=0.03, y=0.96, ha="left", fontsize=21, weight="bold")
fig.text(0.03, 0.88, "Modelo recomendado · profundidade máxima 5", fontsize=12)
for row, column, count, text, background, foreground in [
    (0, 0, tree["tn"], "Normais corretos", TEAL, "white"),
    (0, 1, tree["fp"], "Falsos alarmes", "#FBE4C5", "#763B00"),
    (1, 0, tree["fn"], "Falhas perdidas", "#F7CED0", "#8B2028"),
    (1, 1, tree["tp"], "Falhas detectadas", TEAL, "white"),
]:
    ax.add_patch(Rectangle((column - 0.5, row - 0.5), 1, 1, facecolor=background, edgecolor="white", linewidth=4))
    ax.text(column, row - 0.07, f"{count:,}".replace(",", "."), ha="center", va="center", fontsize=27, weight="bold", color=foreground)
    ax.text(column, row + 0.19, text, ha="center", va="center", fontsize=12, color=foreground)
ax.set(xlim=(-0.5, 1.5), ylim=(1.5, -0.5), aspect="equal")
ax.set_xticks([0, 1], ["Normal", "Falha"])
ax.set_yticks([0, 1], ["Normal", "Falha"])
ax.set_xlabel("Classe prevista", labelpad=10)
ax.set_ylabel("Classe real", labelpad=10)
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
save(fig, "matriz-confusao-arvore.png", "Fonte: notebook, teste preservado. Matriz [[1731, 201], [11, 57]].")
print("Três PNGs gerados em docs/assets/ com dados verificados do notebook.")
