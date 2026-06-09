#!/usr/bin/env python3
"""
图表生成示例脚本。
运行：python3 scripts/generate_figures.py
输出：figures/ 目录下的 PDF 矢量图文件。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "figures"

# 中文字体
_cjk_family = None
for _name in ["Source Han Serif CN", "SimSun", "Noto Serif CJK SC",
              "WenQuanYi Micro Hei", "Noto Sans CJK SC"]:
    for _f in fm.fontManager.ttflist:
        if _f.name == _name:
            _cjk_family = _f.name
            break
    if _cjk_family:
        break

plt.rcParams.update({
    "font.family": _cjk_family or "serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "axes.unicode_minus": False,
})


def bar_chart():
    """柱状图：各模型 BLEU 分数对比"""
    models = ["Transformer\n-base", "BERT\n-fused", "Reformer", "BigBird", "本文方法"]
    en_de  = [27.3, 27.8, 27.1, 26.9, 28.4]
    en_fr  = [38.1, 39.2, 37.5, 37.0, 39.8]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(models))
    w = 0.35
    bars1 = ax.bar(x - w/2, en_de, w, label="EN-DE", color="#2c7fb8", edgecolor="black", linewidth=0.3)
    bars2 = ax.bar(x + w/2, en_fr, w, label="EN-FR", color="#fc8d62", edgecolor="black", linewidth=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("BLEU")
    ax.legend()
    ax.set_ylim(0, 45)
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.1f}", ha="center", fontsize=8)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.1f}", ha="center", fontsize=8)

    path = OUTPUT_DIR / "example_bar.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  ✓ {path}")


def line_chart():
    """折线图：训练 loss 下降曲线"""
    steps = np.arange(0, 50001, 500)
    rng = np.random.default_rng(42)
    loss_baseline = 7.2 * np.exp(-steps / 8000) + 3.8 + rng.normal(0, 0.12, len(steps))
    loss_ours     = 7.5 * np.exp(-steps / 7000) + 3.4 + rng.normal(0, 0.10, len(steps))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, loss_baseline, alpha=0.4, color="#2c7fb8", linewidth=0.5)
    ax.plot(steps, loss_ours,     alpha=0.4, color="#fc8d62", linewidth=0.5)
    # smoothed
    def smooth(y, w=101):
        return np.convolve(y, np.ones(w)/w, mode="same")
    ax.plot(steps, smooth(loss_baseline), label="基线Transformer", color="#2c7fb8", linewidth=1.5)
    ax.plot(steps, smooth(loss_ours),     label="本文方法",       color="#fc8d62", linewidth=1.5)
    ax.set_xlabel("训练步数")
    ax.set_ylabel("交叉熵损失")
    ax.legend()
    ax.grid(True, alpha=0.3)

    path = OUTPUT_DIR / "example_line.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  ✓ {path}")


def architecture_diagram():
    """架构图：Transformer 编码器-解码器示意"""
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    boxes = [
        (1.0, 4.8, "输入嵌入\n+ 位置编码", "#e8f4f8"),
        (4.0, 4.8, "多头自注意力\n+ 残差 & LN", "#fff2cc"),
        (7.0, 4.8, "前馈网络\n+ 残差 & LN", "#fff2cc"),
        (4.0, 2.5, "多头交叉注意力\n+ 残差 & LN", "#d9ead3"),
        (7.0, 2.5, "前馈网络\n+ 残差 & LN", "#d9ead3"),
        (7.0, 0.8, "线性层\n+ Softmax", "#fce5cd"),
    ]
    for x, y, label, color in boxes:
        rect = mpatches.FancyBboxPatch(
            (x, y), 2.0, 1.3, boxstyle="round,pad=0.08",
            facecolor=color, edgecolor="black", linewidth=0.7)
        ax.add_patch(rect)
        ax.text(x + 1.0, y + 0.65, label, ha="center", va="center", fontsize=8)

    # Arrows: encoder
    for sx in [3.0, 6.0]:
        ax.annotate("", xy=(sx + 1.0, 5.45), xytext=(sx, 5.45),
                    arrowprops=dict(arrowstyle="->", color="gray", lw=1.2))
    # Encoder -> Decoder
    ax.annotate("", xy=(4.5, 3.8), xytext=(4.5, 5.45),
                arrowprops=dict(arrowstyle="->", color="gray", lw=1.2, linestyle="dashed"))
    # Decoder flow
    for sx in [4.0, 6.0]:
        ax.annotate("", xy=(sx + 1.0, 3.15), xytext=(sx, 3.15),
                    arrowprops=dict(arrowstyle="->", color="gray", lw=1.2))
    ax.annotate("", xy=(8.0, 2.1), xytext=(8.0, 3.15),
                arrowprops=dict(arrowstyle="->", color="gray", lw=1.2))

    ax.text(5.0, 5.8, "编码器（×N）", ha="center", fontsize=10, fontweight="bold")
    ax.text(5.0, 3.5, "解码器（×N）", ha="center", fontsize=10, fontweight="bold")

    path = OUTPUT_DIR / "example_architecture.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  ✓ {path}")


# ============================================================
if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("生成示例图表：")
    bar_chart()
    line_chart()
    architecture_diagram()
    print("完成。图表输出到 figures/")
