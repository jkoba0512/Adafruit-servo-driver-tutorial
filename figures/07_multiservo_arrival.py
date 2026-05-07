"""Ch 2: 複数サーボに「同時に命令」しても到着時刻はバラバラ"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch2_arrival_times.png"


def main() -> None:
    _style.apply()

    # サーボの最大角速度 ≒ 60° / 0.1s ≒ 600°/s
    # PCA9685 カウントで 1° ≒ 2.5 カウント → 1500 カウント/秒 = 1.5 カウント/ms
    speed_per_ms = 1.5

    targets = [50, 150, 300, 450]   # 動かす距離（PWMカウント）
    colors = [_style.ACCENT[c] for c in ["blue", "green", "orange", "pink"]]
    labels = [f"ch{i} (距離 {d})" for i, d in enumerate(targets)]

    t_max = max(targets) / speed_per_ms * 1.15
    t = np.linspace(0, t_max, 2000)

    fig, ax = plt.subplots(figsize=(10, 5.2))

    for tgt, c, lab in zip(targets, colors, labels):
        pos = np.minimum(t * speed_per_ms, tgt)
        ax.plot(t, pos, color=c, linewidth=2.6, label=lab)
        # 到着点
        t_arr = tgt / speed_per_ms
        ax.scatter([t_arr], [tgt], color=c, s=110, zorder=10,
                   edgecolor=_style.FG, linewidth=1.2)
        ax.annotate(f"{t_arr:.0f} ms", xy=(t_arr, tgt),
                    xytext=(t_arr + 8, tgt - 22),
                    color=c, fontsize=10, weight="bold")

    # 命令タイミング（t=0）
    ax.axvline(0, color=_style.ACCENT["yellow"],
               linestyle="--", linewidth=2)
    ax.text(2, 470, "← t = 0 で全サーボに同時 setPWM",
            color=_style.ACCENT["yellow"], fontsize=11, weight="bold")

    ax.set_xlabel("時間 [ms]")
    ax.set_ylabel("サーボ位置（PWMカウント差分）")
    ax.set_title("命令は同時 → 到着はバラバラ（移動距離が違うから）",
                 fontsize=13, weight="bold")
    ax.set_xlim(-15, t_max)
    ax.set_ylim(0, 510)
    ax.legend(loc="lower right", facecolor=_style.BG, edgecolor=_style.FG,
              fontsize=10)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
