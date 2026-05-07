"""Ch 3: 時間補間 — 全サーボが同じ時刻で目標到達"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch3_sync_interpolation.png"


def main() -> None:
    _style.apply()

    duration = 1000     # ms
    n_steps = 20        # 補間ステップ数

    targets = [120, 280, 480]
    colors = [_style.ACCENT[c] for c in ["blue", "green", "orange"]]
    labels = ["ch0 (短距離 120)", "ch1 (中距離 280)", "ch2 (長距離 480)"]

    fig, ax = plt.subplots(figsize=(10, 5.2))

    t_steps = np.linspace(0, duration, n_steps + 1)
    for tgt, c, lab in zip(targets, colors, labels):
        positions = tgt * (np.arange(n_steps + 1) / n_steps)
        ax.step(t_steps, positions, where="post",
                color=c, linewidth=2.2, label=lab)
        ax.scatter(t_steps, positions, color=c, s=42, zorder=10,
                   edgecolor=_style.FG, linewidth=0.6)

    # 開始・終了の縦線
    ax.axvline(0, color=_style.ACCENT["yellow"],
               linestyle="--", linewidth=1.2, alpha=0.6)
    ax.axvline(duration, color=_style.ACCENT["yellow"],
               linestyle="--", linewidth=2)
    ax.text(duration - 10, 500, "全員同時に到着 ✓",
            ha="right", color=_style.ACCENT["yellow"],
            fontsize=12, weight="bold")
    ax.text(8, 500, "t = 0\nスタート",
            color=_style.ACCENT["yellow"], fontsize=10)

    # 各ラインの右端に「1ステップで動く量」を注釈
    for tgt, c in zip(targets, colors):
        step_size = tgt / n_steps
        ax.annotate(f"1ステップ = {step_size:.0f}",
                    xy=(duration + 5, tgt),
                    xytext=(duration - 250, tgt + 25),
                    color=c, fontsize=9,
                    arrowprops=dict(arrowstyle="->", color=c, lw=0.8))

    ax.set_xlabel("時間 [ms]")
    ax.set_ylabel("サーボ位置（PWMカウント差分）")
    ax.set_title(f"時間補間で同期: 全サーボが duration = {duration}ms で同時到達",
                 fontsize=13, weight="bold")
    ax.set_xlim(-30, duration + 50)
    ax.set_ylim(-10, 540)
    ax.legend(loc="lower right", facecolor=_style.BG, edgecolor=_style.FG,
              fontsize=10)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
