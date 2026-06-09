# 快速开始

## 推荐方式：Docker（零依赖，跨平台）

无需安装 TeX Live、中文字体或 Python —— 只需 [Docker](https://docs.docker.com/get-docker/)。

```bash
# 1. 构建镜像（仅首次，约 5 分钟）
docker build -t hdu-essay-template .

# 2. 编译论文
docker run --rm -v $(pwd):/workdir hdu-essay-template
# → 生成 main.pdf

# 3.（可选）国内代理加速构建
docker build \
  --build-arg HTTP_PROXY=http://proxy:port \
  --build-arg HTTPS_PROXY=http://proxy:port \
  -t hdu-essay-template .
```

> 镜像约 1.5 GB，含完整 TeX Live + 中文字体 + Python 图表生成。

## 本地编译（需自行安装 TeX Live）

```bash
# Fedora
sudo dnf install -y texlive-xetex texlive-ctex texlive-gbt7714 \
  texlive-tocloft texlive-fancyhdr texlive-geometry \
  texlive-{booktabs,mathtools,caption,hyperref,cleveref} \
  texlive-{zhlipsum,enumitem,float,placeins} \
  texlive-stix2-otf \
  adobe-source-han-sans-cn-fonts adobe-source-han-serif-cn-fonts

# Ubuntu / Debian
sudo apt install -y texlive-xetex texlive-latex-extra \
  texlive-lang-chinese texlive-fonts-extra fonts-noto-cjk

# macOS
brew install --cask mactex font-source-han-serif-cn font-source-han-sans-cn
```

编译（需 3 遍解析交叉引用）：

```bash
latexmk -xelatex -interaction=nonstopmode main.tex
# → main.pdf
```

## 填写论文信息

编辑 `main.tex` 的 `\hduset{...}` 块：

```latex
\hduset{
  title      = {论文中文标题/页眉短标题},
  department = 学院全称,
  major      = 专业全称,
  class      = 班级编号,
  stdntid    = 学号,
  author     = 姓名,
  supervisor = ~:指导教师姓名,
}
```

> `title` 以 `/` 分隔封面大标题和页眉标题。"本科毕业设计（论文）" 需包含全角括号。

## 撰写内容

- **章节** → `chapters/` 目录，按 ch01–ch06 依次编辑
- **参考文献** → `references.bib`，GB/T 7714 格式，`\cite{key}` 引用
- **图片** → 放入 `figures/`，推荐 PDF 矢量图
- **表格** → 写入 `tables/`，用 `\input{tables/xxx}` 引入

## 生成图表（可选）

```bash
pip install matplotlib numpy
python3 scripts/generate_figures.py
```
