"""Ch 0: RC サーボの PWM パルス（パルス幅と角度の対応）"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch0_pwm_signal.png"


def square_pulse(t, period, pulse_width):
    """t 配列のうち、各周期の最初 pulse_width [ms] だけ HIGH"""
    phase = t % period
    return (phase < pulse_width).astype(float)


def main() -> None:
    _style.apply()

    period = 20.0     # ms
    cycles_to_show = 1.6
    t = np.linspace(0, period * cycles_to_show, 4000)

    cases = [
        (0.5, "-90°（左いっぱい）", _style.ACCENT["blue"]),
        (1.5, " 0°（中央）",         _style.ACCENT["green"]),
        (2.5, "+90°（右いっぱい）",  _style.ACCENT["orange"]),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True)

    for ax, (pw, label, color) in zip(axes, cases):
        sig = square_pulse(t, period, pw)
        ax.plot(t, sig, color=color, linewidth=2.4)
        ax.fill_between(t, 0, sig, color=color, alpha=0.25, step=None)

        # パルス幅の矢印 + ラベル（最初のパルス）— パルスと被らないよう外に配置
        label_x = max(pw + 1.5, 4.0)
        ax.annotate(f"{pw} ms",
                    xy=(pw, 0.55), xytext=(label_x, 0.55),
                    color=_style.FG, fontsize=10, va="center",
                    arrowprops=dict(arrowstyle="-",
                                    color=_style.FG, lw=1.0))
        ax.annotate("", xy=(pw, 0.4), xytext=(0, 0.4),
                    arrowprops=dict(arrowstyle="<->",
                                    color=_style.FG, lw=1.2))

        # 軸装飾
        ax.set_ylim(-0.15, 1.45)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["LOW", "HIGH"])
        ax.set_ylabel(f"パルス幅 = {pw} ms\n→ {label}",
                      fontsize=10, rotation=0, ha="right", va="center",
                      labelpad=15)
        ax.grid(True, axis="x", alpha=0.3)

    # 上のサブプロットだけ「20 ms 周期」を強調
    ax_top = axes[0]
    ax_top.annotate("", xy=(period, 1.25), xytext=(0, 1.25),
                    arrowprops=dict(arrowstyle="<->",
                                    color=_style.ACCENT["yellow"], lw=2))
    ax_top.text(period / 2, 1.32, "1 周期 = 20 ms (50 Hz)",
                ha="center", color=_style.ACCENT["yellow"],
                fontsize=11, weight="bold")

    axes[-1].set_xlabel("時間 [ms]")
    axes[-1].set_xlim(0, period * cycles_to_show)

    fig.suptitle("RC サーボの PWM 信号 — パルス幅で角度が決まる",
                 fontsize=14, weight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
