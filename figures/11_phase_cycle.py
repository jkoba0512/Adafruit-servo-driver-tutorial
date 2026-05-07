"""Ch 5: 位相 φ の時間進行（鋸波）"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch5_phase_cycle.png"


def main() -> None:
    _style.apply()

    cycle_time = 1.0       # 1サイクルの長さ（任意単位、ここでは "1 cycle"）
    n_cycles = 2.4
    t = np.linspace(0, n_cycles * cycle_time, 2000)
    phase = (t / cycle_time) % 1.0

    fig, ax = plt.subplots(figsize=(10, 4.6))

    # 鋸波：cycle ごとに 0 → 1 → (drop) → 0 → 1 …
    # 単純に plot するとラップ部に縦線が入るため、サイクル毎に区切る
    cycle_indices = np.where(np.diff(phase) < 0)[0]
    starts = np.concatenate(([0], cycle_indices + 1))
    ends = np.concatenate((cycle_indices + 1, [len(t)]))
    for s, e in zip(starts, ends):
        ax.plot(t[s:e], phase[s:e],
                color=_style.ACCENT["blue"], linewidth=2.6)

    # サイクル境界の縦線
    for c in range(int(n_cycles) + 1):
        x = c * cycle_time
        ax.axvline(x, color=_style.FG, linewidth=0.8,
                   linestyle="--", alpha=0.55)

    # 1/4 ごとのマーカー（最初の1サイクル分だけ）
    quarter_phases = [0.0, 0.25, 0.5, 0.75]
    for ph in quarter_phases:
        ax.scatter([ph * cycle_time], [ph],
                   s=85, color=_style.ACCENT["yellow"],
                   zorder=10, edgecolor=_style.FG, linewidth=1.0)
        ax.text(ph * cycle_time, ph + 0.07,
                f"φ = {ph:.2f}",
                color=_style.ACCENT["yellow"],
                fontsize=10, ha="center", weight="bold")

    # ラップアラウンド注釈（1.0 → 0.0）
    ax.annotate("", xy=(1.005, 0.04), xytext=(1.0, 0.96),
                arrowprops=dict(arrowstyle="->",
                                color=_style.ACCENT["pink"],
                                lw=1.8,
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(1.06, 0.5, "1.0 に達したら\n0.0 に戻る",
            color=_style.ACCENT["pink"], fontsize=10,
            ha="left", va="center", weight="bold")

    # サイクル長の注釈（1サイクル目の上に）
    ax.annotate("", xy=(cycle_time, 1.18), xytext=(0, 1.18),
                arrowprops=dict(arrowstyle="<->",
                                color=_style.ACCENT["green"], lw=1.8))
    ax.text(cycle_time / 2, 1.24, "1 サイクル",
            ha="center", color=_style.ACCENT["green"],
            fontsize=11, weight="bold")

    # 軸装飾
    ax.set_xlim(-0.05, n_cycles)
    ax.set_ylim(-0.1, 1.4)
    ax.set_xlabel("時間 t  [サイクル単位]")
    ax.set_ylabel("位相  φ")
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticks(np.arange(0, n_cycles + 0.01, 0.5))
    ax.set_title("位相 φ ∈ [0, 1) の時間進行 — サイクル毎に 0 にリセット",
                 fontsize=13, weight="bold")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
