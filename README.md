# 杭州电子科技大学本科毕业论文 LaTeX 模板

基于 [hduthesis](https://github.com/myhsia/hduthesis) v1.1.1 文档类，经验证适配杭州电子科技大学本科毕业论文格式要求。

> **[快速开始](QUICKSTART.md)**（Docker 零依赖，3 条命令出 PDF）

## 示例 PDF

编译后的示例：[main.pdf](main.pdf)

## 目录结构

```
HDU-ESSAY-TEMPLATE-TEX/
├── README.md                   # 本文件
├── QUICKSTART.md               # 快速开始（Docker / 本地编译）
├── main.tex                    # 主文档（填入元信息后直接编译）
├── references.bib              # 参考文献数据库
│
├── hduthesis.cls               # 杭电论文文档类（勿修改）
├── hdu-bc.config.code.tex      # 本科配置：封面/摘要/目录/章节格式
├── hdu-layout.code.tex         # 页面布局：页眉页脚/几何设置
├── hdu-typeset.code.tex        # 字体与排版设置
│
├── hdu-logo.pdf                # 校徽
├── hdu-title.pdf               # 校名
├── hdu-badge.pdf               # 徽章
│
├── chapters/                   # 章节目录
│   ├── ch01_introduction.tex   # 第1章 绪论
│   ├── ch02_background.tex     # 第2章 理论基础
│   ├── ch03_design.tex         # 第3章 系统设计
│   ├── ch04_optimization.tex   # 第4章 实现与优化
│   ├── ch05_experiments.tex    # 第5章 实验分析
│   └── ch06_conclusion.tex     # 第6章 总结展望
│
├── figures/                    # 存放图片（PDF/PNG）
│   └── .gitkeep
│
├── tables/                     # 独立表格文件
│   ├── example_threeline.tex   # 三线表示例
│   ├── example_boxed.tex       # 全框线表格示例
│   └── example_env.tex         # 环境配置表示例
│
└── scripts/
    └── generate_figures.py     # matplotlib 图表生成示例
```

## 格式规范

依据《杭州电子科技大学毕业设计（论文）的写作规范和参考格式》：

| 项目   | 设置                                       |
| ---- | ---------------------------------------- |
| 纸张   | A4 (210mm × 297mm)                       |
| 页边距  | 上 3cm、下 2cm、左 3cm、右 2cm                  |
| 正文字号 | 小四 (12pt)，行距 20 磅                        |
| 封面   | 大标题 "本科毕业设计（论文）" 散布排布（35pt 等效），填写内容楷体小三号 |
| 诚信承诺 | 自动生成                                     |
| 摘要   | 中文 + 英文，各一页，无页码                          |
| 目录   | "目录" 黑体三号居中；目录页码为罗马数字（I），自动编号            |
| 章节标题 | 第一级黑体三号居中，第二级黑体四号，第三级黑体小四号               |
| 页眉   | 居中 "杭州电子科技大学本科毕业设计（论文）"，宋体五号             |
| 页码   | 正文阿拉伯数字 Times New Roman 五号居中             |
| 参考文献 | GB/T 7714 国标格式，按引用顺序编号                   |
| 图表编号 | `章-序号`（如 "图3-1"、"表4-2"）                  |

## 用法速览

### 表格

```latex
% 外置文件（推荐）
\input{tables/example_threeline}

% 正文内嵌
\begin{table}[ht]
\centering
\caption{表格标题}
\label{tab:my_label}
\begin{tabular}{lcc}
\hline
列1 & 列2 & 列3 \\
\hline
数据 & 数据 & 数据 \\
\hline
\end{tabular}
\end{table}
```

### 图片

```latex
\begin{figure}[ht]
\centering
\includegraphics[width=0.8\textwidth]{figures/your_figure.pdf}
\caption{图片标题}
\label{fig:my_label}
\end{figure}
```

### 交叉引用

```latex
图\ref{fig:my_label}     % → "图3-1"
表\ref{tab:my_label}     % → "表4-2"
式\ref{eq:my_equation}   % → "公式(5-3)"
```

## 致谢

- 模板基于 [hduthesis](https://github.com/myhsia/hduthesis)
