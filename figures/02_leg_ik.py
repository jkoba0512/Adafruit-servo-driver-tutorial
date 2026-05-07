"""Ch 4: 2-DOF 脚の逆運動学（IK）— 余弦定理で角度を求める

膝前構成（theta_hip = alpha + beta）で「自然な立ち姿勢」を可視化する。
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch4_leg_ik.png"


def main() -> None:
    _style.apply()

    # リンク長と足先（膝前で自然な立ち姿勢になる位置）
    L1, L2 = 50.0, 60.0
    foot_x, foot_y = 20.0, 95.0

    # IK 解（膝前構成）
    d = np.hypot(foot_x, foot_y)
    alpha = np.arctan2(foot_x, foot_y)
    cos_beta = (L1 ** 2 + d ** 2 - L2 ** 2) / (2 * L1 * d)
    beta = np.arccos(np.clip(cos_beta, -1, 1))
    cos_gamma = (L1 ** 2 + L2 ** 2 - d ** 2) / (2 * L1 * L2)
    gamma = np.arccos(np.clip(cos_gamma, -1, 1))

    theta_hip = alpha + beta  # ★膝前を選ぶ
    knee_x = L1 * np.sin(theta_hip)
    knee_y = L1 * np.cos(theta_hip)

    fig, ax = plt.subplots(figsize=(8.5, 7.5))

    # 軸：原点を hip にして X 前方+, Y 下向き+（matplotlib では y 反転で描く）
    ax.invert_yaxis()
    ax.set_aspect("equal")

    # ボディ参照
    ax.add_patch(plt.Rectangle((-15, -12), 30, 9, facecolor=_style.GRID,
                               edgecolor=_style.FG, linewidth=1, alpha=0.5))
    ax.text(0, -16, "ボディ", ha="center", va="bottom",
            color=_style.FG, fontsize=10)

    # 真下方向の補助線
    ax.plot([0, 0], [-5, 115], color=_style.FG, linewidth=0.8, linestyle=":",
            alpha=0.5)
    ax.text(2, 65, "真下方向", color=_style.FG, fontsize=9, alpha=0.7,
            rotation=90, va="center")

    # hip-foot 補助線 d
    ax.plot([0, foot_x], [0, foot_y], color=_style.ACCENT["orange"],
            linewidth=1.5, linestyle="--", alpha=0.8,
            label=f"d (hip→foot) = {d:.1f} mm")

    # リンク（大腿・脛）
    ax.plot([0, knee_x], [0, knee_y], color=_style.ACCENT["blue"],
            linewidth=5, label=f"L₁ (大腿) = {L1:.0f} mm",
            solid_capstyle="round")
    ax.plot([knee_x, foot_x], [knee_y, foot_y], color=_style.ACCENT["green"],
            linewidth=5, label=f"L₂ (脛) = {L2:.0f} mm",
            solid_capstyle="round")

    # 関節と足先のマーカー
    for (px, py, label, dx, dy, ha) in [
        (0, 0, "hip", -7, -3, "right"),
        (knee_x, knee_y, "knee", 4, 0, "left"),
        (foot_x, foot_y, "foot (x, y)", 4, 2, "left"),
    ]:
        ax.scatter([px], [py], s=140, color=_style.ACCENT["pink"], zorder=10,
                   edgecolor=_style.FG, linewidth=1.4)
        ax.text(px + dx, py + dy, label, color=_style.FG, fontsize=12,
                ha=ha, va="center")

    # 角度 α（真下から d 方向）— hip 周りの円弧
    a_arc = np.linspace(np.pi / 2 - alpha, np.pi / 2, 40)
    r_a = 14
    ax.plot(r_a * np.cos(a_arc), r_a * np.sin(a_arc),
            color=_style.ACCENT["yellow"], linewidth=2.5)
    a_mid = np.pi / 2 - alpha / 2
    ax.text(20 * np.cos(a_mid), 20 * np.sin(a_mid),
            r"$\alpha$", color=_style.ACCENT["yellow"],
            fontsize=15, ha="center", va="center", weight="bold")

    # 角度 β（hip-foot と大腿の間）— hip 周りの円弧（外側）
    b_arc = np.linspace(np.pi / 2 - alpha, np.pi / 2 - theta_hip, 40)
    r_b = 26
    ax.plot(r_b * np.cos(b_arc), r_b * np.sin(b_arc),
            color=_style.ACCENT["purple"], linewidth=2.5)
    b_mid = np.pi / 2 - (alpha + theta_hip) / 2
    ax.text(33 * np.cos(b_mid), 33 * np.sin(b_mid),
            r"$\beta$", color=_style.ACCENT["purple"],
            fontsize=15, ha="center", va="center", weight="bold")

    # 角度 γ（膝の内角）— 二等分線ベースで短い側の円弧を描く
    v_hip = np.array([0 - knee_x, 0 - knee_y])
    v_foot = np.array([foot_x - knee_x, foot_y - knee_y])
    bisector = v_hip / np.linalg.norm(v_hip) + v_foot / np.linalg.norm(v_foot)
    g_mid_ang = np.arctan2(bisector[1], bisector[0])
    g_arc = np.linspace(g_mid_ang - gamma / 2, g_mid_ang + gamma / 2, 40)
    r_g = 12
    ax.plot(knee_x + r_g * np.cos(g_arc), knee_y + r_g * np.sin(g_arc),
            color=_style.ACCENT["orange"], linewidth=2.5)
    ax.text(knee_x + 20 * np.cos(g_mid_ang),
            knee_y + 20 * np.sin(g_mid_ang),
            r"$\gamma$", color=_style.ACCENT["orange"],
            fontsize=15, ha="center", va="center", weight="bold")

    # 軸ラベル・タイトル
    ax.set_xlabel("X  前方 [mm]")
    ax.set_ylabel("Y  下方向 [mm]")
    ax.set_title("2-DOF 脚の IK：余弦定理で角度を求める（膝前構成）")
    ax.set_xlim(-55, 75)
    ax.set_ylim(125, -30)
    ax.legend(loc="lower right", facecolor=_style.BG, edgecolor=_style.FG,
              fontsize=10, framealpha=0.9)

    # 解説テキスト（左下に配置、軸とは被らない位置）
    formula = (
        r"$d = \sqrt{x^2 + y^2}$" + "\n"
        r"$\alpha = \mathrm{atan2}(x, y)$" + "\n"
        r"$\cos\beta = \dfrac{L_1^2 + d^2 - L_2^2}{2\,L_1\,d}$" + "\n"
        r"$\cos\gamma = \dfrac{L_1^2 + L_2^2 - d^2}{2\,L_1\,L_2}$" + "\n"
        r"$\theta_{hip} = \alpha + \beta$" + "\n"
        r"$\theta_{knee} = \pi - \gamma$"
    )
    ax.text(-52, 122, formula, color=_style.FG, fontsize=11,
            verticalalignment="bottom", horizontalalignment="left",
            bbox=dict(facecolor=_style.GRID, edgecolor=_style.FG,
                      alpha=0.55, boxstyle="round,pad=0.5"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
