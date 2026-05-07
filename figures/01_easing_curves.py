"""Ch 3: 線形補間 vs smoothstep の比較カーブ"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch3_easing.png"


def main() -> None:
    _style.apply()

    t = np.linspace(0.0, 1.0, 200)
    linear = t
    smooth = t * t * (3.0 - 2.0 * t)

    fig, ax = plt.subplots(figsize=(7.0, 5.0))

    ax.plot(t, linear, color=_style.ACCENT["blue"], linewidth=2.5,
            label="線形補間 (lerp)")
    ax.plot(t, smooth, color=_style.ACCENT["orange"], linewidth=2.5,
            label="smoothstep $t^2(3-2t)$")

    # 補助：両端点
    ax.scatter([0, 1], [0, 0], color=_style.FG, s=40, zorder=5)
    ax.scatter([0, 1], [1, 1], color=_style.FG, s=40, zorder=5)

    ax.set_xlabel("経過時間の比率  t = elapsed / duration")
    ax.set_ylabel("位置の進捗  ratio")
    ax.set_title("補間カーブの比較")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="lower right", facecolor=_style.BG, edgecolor=_style.FG)

    # 解説文を内側に
    ax.text(0.02, 0.92,
            "lerp: 等速で動く（始めと終わりが急）",
            color=_style.ACCENT["blue"], fontsize=11)
    ax.text(0.02, 0.85,
            "smoothstep: 滑らかに加減速（モータに優しい）",
            color=_style.ACCENT["orange"], fontsize=11)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
