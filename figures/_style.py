"""ダークモード用の共通スタイル設定（just-the-docs dark に合わせる）"""
import matplotlib.pyplot as plt

BG = "#27262b"      # 背景（just-the-docs dark の body bg）
FG = "#e6e1e8"      # 文字・軸（just-the-docs dark の text）
GRID = "#444444"

# 強調色（カラーブラインドフレンドリー寄り）
ACCENT = {
    "blue":   "#5ec4ff",
    "orange": "#ffb86c",
    "green":  "#9ce884",
    "pink":   "#ff79c6",
    "yellow": "#f1fa8c",
    "purple": "#bd93f9",
}


def apply():
    plt.rcParams.update({
        "figure.facecolor": BG,
        "savefig.facecolor": BG,
        "axes.facecolor": BG,
        "axes.edgecolor": FG,
        "axes.labelcolor": FG,
        "axes.titlecolor": FG,
        "text.color": FG,
        "xtick.color": FG,
        "ytick.color": FG,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linestyle": "--",
        "grid.alpha": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "figure.dpi": 120,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        # 日本語フォント（macOS）
        "font.family": ["Hiragino Sans", "Yu Gothic", "DejaVu Sans"],
        "axes.unicode_minus": False,
    })
