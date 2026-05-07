"""Ch 1: PCA9685 ch0 の 3pin とサーボケーブルの色対応"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch1_servo_3pin.png"


def main() -> None:
    _style.apply()

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.set_aspect("equal")
    ax.axis("off")

    # ===== PCA9685 側の 3pin =====
    pin_y = 1.5
    pin_w = 1.4
    pin_h = 0.85
    pins = [
        (0.0, "PWM", "信号"),
        (1.6, "V+",  "電源 (+5V)"),
        (3.2, "GND", "グラウンド"),
    ]
    for x, name, desc in pins:
        # ピン本体
        ax.add_patch(Rectangle((x, pin_y), pin_w, pin_h,
                               facecolor=_style.GRID,
                               edgecolor=_style.FG, linewidth=1.6))
        ax.text(x + pin_w / 2, pin_y + pin_h / 2, name,
                ha="center", va="center",
                color=_style.FG, fontsize=15, weight="bold")
        # 説明
        ax.text(x + pin_w / 2, pin_y + pin_h + 0.18, desc,
                ha="center", va="bottom",
                color=_style.FG, fontsize=10, alpha=0.85)

    # PCA9685 ラベル
    ax.text(2.3, pin_y + pin_h + 0.7, "PCA9685 ch0 の 3pin",
            ha="center", color=_style.FG, fontsize=13, weight="bold")

    # ===== サーボケーブル =====
    cable_y = -0.6
    wire_specs = [
        ("橙 / 黄 / 白", _style.ACCENT["orange"]),
        ("赤",            "#ff5544"),
        ("茶 / 黒",       "#7a4a3b"),
    ]
    for (x, _, _), (cname, c) in zip(pins, wire_specs):
        cx = x + pin_w / 2
        # ケーブル線
        ax.plot([cx, cx], [pin_y - 0.05, cable_y + 0.4],
                color=c, linewidth=10, solid_capstyle="round")
        # コネクタ筐体
        ax.add_patch(FancyBboxPatch((cx - 0.45, cable_y - 0.05), 0.9, 0.45,
                                    boxstyle="round,pad=0.04",
                                    facecolor="#1a1a1a",
                                    edgecolor=_style.FG, linewidth=1))
        # 色ラベル
        ax.text(cx, cable_y - 0.4, cname,
                ha="center", va="top", color=c,
                fontsize=11, weight="bold")

    # 注記
    ax.text(2.3, cable_y - 1.1,
            "サーボのケーブル（色は機種で異なる — 表参照）",
            ha="center", color=_style.FG, fontsize=10, alpha=0.7)

    # 真ん中=+V のハイライト矢印
    ax.annotate("", xy=(2.3, pin_y - 0.05), xytext=(2.3, cable_y + 0.5),
                arrowprops=dict(arrowstyle="-", color=_style.ACCENT["yellow"],
                                lw=0))  # marker のみ
    ax.text(4.9, (pin_y + cable_y) / 2 + 0.5,
            "★ 真ん中は\n常に +V (赤)",
            ha="left", va="center",
            color=_style.ACCENT["yellow"],
            fontsize=11, weight="bold",
            bbox=dict(facecolor=_style.GRID, edgecolor=_style.ACCENT["yellow"],
                      boxstyle="round,pad=0.3", alpha=0.8))

    ax.set_xlim(-0.6, 7.0)
    ax.set_ylim(-2.2, 3.2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
