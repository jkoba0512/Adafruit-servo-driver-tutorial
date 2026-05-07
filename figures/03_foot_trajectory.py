"""Ch 5: 足先のスイング+スタンス軌道（1サイクル）"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch5_foot_trajectory.png"


def main() -> None:
    _style.apply()

    # 歩行パラメータ
    duty = 0.75
    swing_dur = 1.0 - duty
    stride = 60.0
    step_height = 25.0
    z_default = 100.0  # 接地高さ（下向きが +）

    # phase 0..1
    p = np.linspace(0.0, 1.0, 400)
    xf = np.zeros_like(p)
    zd = np.zeros_like(p)

    swing_mask = p < swing_dur
    u_sw = p[swing_mask] / swing_dur
    xf[swing_mask] = -stride / 2 + stride * u_sw
    zd[swing_mask] = z_default - step_height * np.sin(np.pi * u_sw)

    stance_mask = ~swing_mask
    u_st = (p[stance_mask] - swing_dur) / duty
    xf[stance_mask] = stride / 2 - stride * u_st
    zd[stance_mask] = z_default

    # サブプロット 2 段
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 7.0),
                                   gridspec_kw={"height_ratios": [3, 2]})

    # ===== 上段：側面図 (X-Z) =====
    ax1.invert_yaxis()  # Y は下向きが正
    ax1.set_aspect("equal")

    # 地面
    ax1.axhline(z_default, color=_style.FG, linestyle="-",
                linewidth=1, alpha=0.5)
    ax1.fill_between([-50, 50], z_default, 130,
                     color=_style.GRID, alpha=0.3, hatch="//")
    ax1.text(45, z_default + 4, "地面", color=_style.FG,
             fontsize=10, ha="right", va="top", alpha=0.7)

    # 軌道（スイングとスタンスを色分け）
    ax1.plot(xf[swing_mask], zd[swing_mask],
             color=_style.ACCENT["blue"], linewidth=3,
             label=f"スイング期 (duty={1-duty:.2f})")
    ax1.plot(xf[stance_mask], zd[stance_mask],
             color=_style.ACCENT["orange"], linewidth=3,
             label=f"スタンス期 (duty={duty:.2f})")

    # 進行方向矢印
    ax1.annotate("", xy=(stride/2 + 5, 70), xytext=(stride/2 - 5, 70),
                 arrowprops=dict(arrowstyle="->", color=_style.ACCENT["green"],
                                 linewidth=2))
    ax1.text(stride/2, 65, "ボディ進行方向", color=_style.ACCENT["green"],
             fontsize=10, ha="center")

    # 開始/終了点
    ax1.scatter([xf[0]], [zd[0]], s=100, color=_style.ACCENT["pink"],
                zorder=10, edgecolor=_style.FG, linewidth=1)
    ax1.text(xf[0] - 3, zd[0] - 3, "start", color=_style.FG,
             fontsize=10, ha="right")

    ax1.set_xlabel("X  前後位置 [mm]  (前方+)")
    ax1.set_ylabel("Z  足先深さ [mm]  (下方向+)")
    ax1.set_title("1脚分の足先軌道（1サイクル）")
    ax1.set_xlim(-45, 55)
    ax1.set_ylim(125, 55)
    ax1.legend(loc="upper right", facecolor=_style.BG, edgecolor=_style.FG,
               fontsize=10)

    # ===== 下段：phase に対する xf, zd =====
    ax2.plot(p, xf, color=_style.ACCENT["blue"], linewidth=2,
             label="X (前後)")
    ax2.plot(p, zd, color=_style.ACCENT["orange"], linewidth=2,
             label="Z (深さ)")

    # スイング期を背景でハイライト
    ax2.axvspan(0, swing_dur, color=_style.ACCENT["blue"], alpha=0.12,
                label="スイング期")
    ax2.axvspan(swing_dur, 1.0, color=_style.ACCENT["orange"], alpha=0.12,
                label="スタンス期")

    ax2.set_xlabel("φ  歩行位相 (0〜1)")
    ax2.set_ylabel("位置 [mm]")
    ax2.set_title("位相に対する X / Z の時系列")
    ax2.set_xlim(0, 1)
    ax2.legend(loc="upper right", facecolor=_style.BG, edgecolor=_style.FG,
               fontsize=9, ncol=2)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
