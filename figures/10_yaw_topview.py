"""Ch 4: 3-DOF への拡張 — 股ヨー（hip yaw）の上面図"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch4_yaw_topview.png"


def main() -> None:
    _style.apply()

    fig, ax = plt.subplots(figsize=(8.5, 7.0))
    ax.set_aspect("equal")
    ax.axis("off")

    # ===== ボディ（上面） =====
    body_w, body_h = 90, 55
    body_x, body_y = -110, -27.5
    ax.add_patch(Rectangle((body_x, body_y), body_w, body_h,
                           facecolor=_style.GRID, edgecolor=_style.FG,
                           linewidth=1.5, alpha=0.55))
    ax.text(body_x + body_w / 2, body_y + body_h / 2, "ロボット\nボディ",
            ha="center", va="center", color=_style.FG, fontsize=11)

    # ===== Hip（前右脚の付け根） =====
    hip_x, hip_y = -20, 0
    ax.scatter([hip_x], [hip_y], s=170, color=_style.ACCENT["pink"],
               zorder=10, edgecolor=_style.FG, linewidth=1.4)
    ax.text(hip_x - 5, hip_y - 9, "hip\n(股関節)", color=_style.FG,
            fontsize=10, ha="right", va="top")

    # ===== 座標軸（hip ローカル） =====
    arrow_len = 55
    # X 軸：前方（画像の上方向）
    ax.annotate("", xy=(hip_x, hip_y + arrow_len), xytext=(hip_x, hip_y),
                arrowprops=dict(arrowstyle="->", color=_style.FG, lw=1.5))
    ax.text(hip_x - 5, hip_y + arrow_len, "+X (前方)\nx_forward",
            color=_style.FG, fontsize=10, ha="right", va="top")

    # Y 軸：横（画像の右方向）
    ax.annotate("", xy=(hip_x + arrow_len, hip_y), xytext=(hip_x, hip_y),
                arrowprops=dict(arrowstyle="->", color=_style.FG, lw=1.5))
    ax.text(hip_x + arrow_len + 4, hip_y - 5, "+Y\n(横, 右)\ny_side",
            color=_style.FG, fontsize=10, ha="left", va="top")

    # ===== 足先（xf, ys 指定） =====
    xf, ys = 45, 30
    foot_x = hip_x + ys     # +Y は画像の右
    foot_y = hip_y + xf     # +X は画像の上

    # 補助線：足先から各軸への垂線
    ax.plot([hip_x, foot_x], [foot_y, foot_y], color=_style.FG,
            linewidth=0.8, linestyle=":", alpha=0.5)
    ax.plot([foot_x, foot_x], [hip_y, foot_y], color=_style.FG,
            linewidth=0.8, linestyle=":", alpha=0.5)
    ax.text((hip_x + foot_x) / 2, foot_y + 2, f"y_side = {ys}",
            color=_style.FG, fontsize=9, ha="center", alpha=0.8)
    ax.text(foot_x + 2, (hip_y + foot_y) / 2, f"x_forward = {xf}",
            color=_style.FG, fontsize=9, ha="left", va="center", alpha=0.8)

    # 脚の水平投影（hip → foot を結ぶ線）
    ax.plot([hip_x, foot_x], [hip_y, foot_y],
            color=_style.ACCENT["green"], linewidth=4.5,
            solid_capstyle="round")

    # x_plane ラベル（線の右下に矢印で引き出す。ボディ下の空き領域へ）
    xp = np.hypot(xf, ys)
    ax.annotate(f"$x_\\mathrm{{plane}} \\approx {xp:.1f}$",
                xy=((hip_x + foot_x) / 2, (hip_y + foot_y) / 2),
                xytext=(35, -55),
                color=_style.ACCENT["green"], fontsize=12, weight="bold",
                ha="center",
                arrowprops=dict(arrowstyle="-",
                                color=_style.ACCENT["green"], lw=1, alpha=0.7))

    # 足先マーカー
    ax.scatter([foot_x], [foot_y], s=140, color=_style.ACCENT["pink"],
               zorder=10, edgecolor=_style.FG, linewidth=1.2)
    ax.text(foot_x + 4, foot_y + 3,
            f"foot (上面投影)\n(x={xf}, y={ys})",
            color=_style.FG, fontsize=10, ha="left", va="bottom")

    # ===== ヨー角 ψ =====
    yaw = np.arctan2(ys, xf)   # +X からの角度
    arc_r = 32
    # +X 方向（画像の上）から脚方向への弧
    arc = np.linspace(np.pi / 2 - yaw, np.pi / 2, 40)
    ax.plot(hip_x + arc_r * np.cos(arc), hip_y + arc_r * np.sin(arc),
            color=_style.ACCENT["yellow"], linewidth=2.5)
    # ラベル
    mid = np.pi / 2 - yaw / 2
    ax.text(hip_x + 42 * np.cos(mid), hip_y + 42 * np.sin(mid),
            r"$\psi_\mathrm{yaw}$",
            color=_style.ACCENT["yellow"],
            fontsize=14, weight="bold", ha="center", va="center")

    # ===== タイトル =====
    ax.text(-15, 90, "上面図（真上から見る） — 股ヨーの定義",
            color=_style.FG, fontsize=13, weight="bold", ha="center")

    # ===== 数式 =====
    formula = (
        r"$\psi_\mathrm{yaw} = \mathrm{atan2}(y_\mathrm{side},\ x_\mathrm{forward})$"
        + "\n"
        r"$x_\mathrm{plane} = \sqrt{x_\mathrm{forward}^2 + y_\mathrm{side}^2}$"
        + "\n\n"
        "$\\rightarrow$ あとは ($x_\\mathrm{plane}$, $z_\\mathrm{down}$) で\n"
        "    Ch 4 前半の 2-DOF IK を適用"
    )
    ax.text(-145, -45, formula, color=_style.FG, fontsize=10,
            verticalalignment="top", horizontalalignment="left",
            bbox=dict(facecolor=_style.GRID, edgecolor=_style.FG,
                      alpha=0.55, boxstyle="round,pad=0.5"))

    ax.set_xlim(-155, 95)
    ax.set_ylim(-85, 95)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
