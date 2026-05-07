"""Ch 1: setPWM(ch, on, off) の動作 — 12bit カウンタと出力の関係"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch1_setpwm_counter.png"


def main() -> None:
    _style.apply()

    on_count = 0
    off_count = 307     # ≒ 1.5 ms (50Hz, 1tick=4.88us)
    counts = np.arange(0, 4096)
    output = np.where((counts >= on_count) & (counts < off_count), 1, 0)

    fig, ax = plt.subplots(figsize=(10, 4.5))

    # PWM 出力
    ax.fill_between(counts, 0, output, step="post",
                    color=_style.ACCENT["blue"], alpha=0.3)
    ax.step(counts, output, where="post",
            color=_style.ACCENT["blue"], linewidth=2.2)

    # on / off の縦線
    ax.axvline(on_count, color=_style.ACCENT["green"],
               linestyle="--", linewidth=2)
    ax.text(on_count + 30, 1.15, f"on = {on_count}",
            ha="left", color=_style.ACCENT["green"],
            weight="bold", fontsize=11)

    ax.axvline(off_count, color=_style.ACCENT["pink"],
               linestyle="--", linewidth=2)
    ax.text(off_count + 30, 1.15, f"off = {off_count}",
            ha="left", color=_style.ACCENT["pink"],
            weight="bold", fontsize=11)

    # パルス幅注釈
    ax.annotate("", xy=(off_count, 0.5), xytext=(on_count, 0.5),
                arrowprops=dict(arrowstyle="<->", color=_style.FG, lw=1.5))
    pw_us = (off_count - on_count) * 4.88
    pw_ms = pw_us / 1000.0
    ax.text((on_count + off_count) / 2, 0.62,
            f"HIGH カウント = {off_count - on_count}\n≒ {pw_us:.0f} µs ≒ {pw_ms:.2f} ms",
            ha="center", color=_style.FG, fontsize=10)

    # 1周期分の注釈
    ax.annotate("", xy=(4095, -0.18), xytext=(0, -0.18),
                arrowprops=dict(arrowstyle="<->",
                                color=_style.ACCENT["yellow"], lw=1.5))
    ax.text(2047, -0.27, "1 周期 = 4096 カウント = 20 ms (50 Hz 設定時)",
            ha="center", color=_style.ACCENT["yellow"], fontsize=10)

    ax.set_xlim(-50, 4150)
    ax.set_ylim(-0.4, 1.45)
    ax.set_xticks([0, 1024, 2048, 3072, 4095])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["LOW", "HIGH"])
    ax.set_xlabel("12-bit カウンタ値 (0 〜 4095)")
    ax.set_title("setPWM(ch, on={}, off={}) の出力イメージ".format(
        on_count, off_count), fontsize=13, weight="bold")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
