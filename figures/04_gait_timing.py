"""Ch 5: 4脚ゲイトの位相タイミング図（クロール vs トロット）"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import _style

OUT = Path(__file__).resolve().parents[1] / "assets" / "images" / "ch5_gait_timing.png"


LEG_NAMES = ["FR (前右)", "FL (前左)", "RR (後右)", "RL (後左)"]


def draw_one(ax, offsets, duty, title):
    """1つのゲイトを横棒で描画"""
    n_legs = len(offsets)
    swing_dur = 1.0 - duty
    cycles_to_show = 1.5  # 位相のラップアラウンドが見えるよう少し長めに

    # 各脚を 1 行で描画
    for i, off in enumerate(offsets):
        y = n_legs - 1 - i  # 上から FR, FL, RR, RL
        # phase = (t + off) mod 1
        # phase < swing_dur => SWING, else STANCE
        # 0 <= t <= cycles_to_show
        # t を細かく刻んで色分け
        ts = np.linspace(0, cycles_to_show, 1000)
        phases = (ts + off) % 1.0
        is_swing = phases < swing_dur
        # スイング期間を青、スタンス期間を橙で塗る
        # 連続区間を見つけて区間ごとに描画
        change_idx = np.where(np.diff(is_swing.astype(int)) != 0)[0]
        starts = np.concatenate(([0], change_idx + 1))
        ends = np.concatenate((change_idx + 1, [len(ts)]))
        for s, e in zip(starts, ends):
            color = _style.ACCENT["blue"] if is_swing[s] else _style.ACCENT["orange"]
            ax.barh(y, ts[e - 1] - ts[s], left=ts[s], height=0.6,
                    color=color, edgecolor=_style.FG, linewidth=0.4)

    # 1サイクル境界の縦線
    for c in range(int(cycles_to_show) + 1):
        ax.axvline(c, color=_style.FG, linewidth=0.6, linestyle="--",
                   alpha=0.5)

    ax.set_yticks(range(n_legs))
    ax.set_yticklabels(list(reversed(LEG_NAMES)), fontsize=11)
    ax.set_xlim(0, cycles_to_show)
    ax.set_xlabel("位相 φ (1サイクル = 1.0)")
    ax.set_title(title)
    ax.set_xticks(np.arange(0, cycles_to_show + 0.01, 0.25))
    ax.grid(True, axis="x", alpha=0.3)


def main() -> None:
    _style.apply()

    fig, axes = plt.subplots(2, 1, figsize=(10, 7),
                             gridspec_kw={"hspace": 0.45})

    # クロール（4-beat walk）: FR=0, FL=0.5, RR=0.75, RL=0.25, duty=0.75
    draw_one(axes[0], offsets=[0.00, 0.50, 0.75, 0.25], duty=0.75,
             title="クロール（duty = 0.75, 1脚ずつ持ち上げ）")

    # トロット（2-beat diagonal）: FR=0, FL=0.5, RR=0.5, RL=0, duty=0.5
    draw_one(axes[1], offsets=[0.00, 0.50, 0.50, 0.00], duty=0.50,
             title="トロット（duty = 0.50, 対角ペア同時）")

    # 共通の凡例
    legend_handles = [
        mpatches.Patch(facecolor=_style.ACCENT["blue"], edgecolor=_style.FG,
                       label="スイング期 (足上げ)"),
        mpatches.Patch(facecolor=_style.ACCENT["orange"], edgecolor=_style.FG,
                       label="スタンス期 (接地)"),
    ]
    fig.legend(handles=legend_handles, loc="upper center",
               bbox_to_anchor=(0.5, 0.99), ncol=2,
               facecolor=_style.BG, edgecolor=_style.FG, fontsize=11)

    fig.suptitle("4脚ゲイトの位相タイミング", fontsize=15, weight="bold",
                 y=1.04)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
