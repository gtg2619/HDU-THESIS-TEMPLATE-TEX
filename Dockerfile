# ============================================================
#  HDU-ESSAY-TEMPLATE-TEX 编译环境
#  杭州电子科技大学本科毕业论文 LaTeX 模板
#  基于 Fedora 44 + TeX Live + XeLaTeX
#
#  构建:
#    docker build -t hdu-essay-template .
#  使用代理构建:
#    docker build --build-arg HTTP_PROXY=http://proxy:port \
#                 --build-arg HTTPS_PROXY=http://proxy:port \
#                 -t hdu-essay-template .
#  提取 PDF:
#    docker run --rm -v $(pwd):/workdir hdu-essay-template
#
#  注意:
#    - 需要稳定的网络连接以从 Fedora 镜像下载 ~500 个包
#    - 国内用户建议配置代理或使用镜像加速
# ============================================================

FROM fedora:44

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY=localhost,127.0.0.1
ENV HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY=${NO_PROXY}

# DNF 代理配置（有代理时启用）
RUN if [ -n "$HTTP_PROXY" ]; then \
      echo "proxy=${HTTP_PROXY}" >> /etc/dnf/dnf.conf; \
      echo "=== DNF proxy: ${HTTP_PROXY} ==="; \
    fi

# ============================================================
#  安装系统依赖
#  --skip-unavailable: 跳过 F44 中已内置或不存在的包（如 array, multicol）
#  timeout=300: 单包超时 5 分钟
#  retries=20:  失败重试 20 次
# ============================================================
RUN dnf install -y \
      --setopt=timeout=300 \
      --setopt=retries=20 \
      --setopt=minrate=0 \
      --setopt=max_parallel_downloads=3 \
      --skip-unavailable \
    \
    # ---- TeX 引擎与核心 ----
    texlive-xetex \
    texlive-bibtex \
    texlive-collection-latex \
    texlive-collection-latexrecommended \
    \
    # ---- 中文 / CJK 支持 ----
    texlive-ctex \
    texlive-fontspec \
    texlive-unicode-math \
    texlive-xecjk \
    texlive-gbt7714 \
    \
    # ---- hdu-typeset.code.tex 依赖 ----
    # circuitikz, pgfplots, listings, hologo, lipsum, zhlipsum,
    # booktabs, mathtools, amssymb, cancel, fixdif,
    # derivative, siunitx, physics2, bm
    texlive-circuitikz \
    texlive-pgfplots \
    texlive-listings \
    texlive-hologo \
    texlive-lipsum \
    texlive-zhlipsum \
    texlive-booktabs \
    texlive-mathtools \
    texlive-amssymb \
    texlive-cancel \
    texlive-fixdif \
    texlive-derivative \
    texlive-siunitx \
    texlive-physics2 \
    texlive-bm \
    \
    # ---- hdu-layout.code.tex 依赖 ----
    texlive-geometry \
    texlive-setspace \
    \
    # ---- hdu-bc.config.code.tex 依赖 ----
    texlive-tocloft \
    \
    # ---- 通用工具宏包 ----
    texlive-colortbl \
    texlive-etoolbox \
    texlive-enumitem \
    texlive-fancyhdr \
    texlive-hyperref \
    texlive-caption \
    texlive-float \
    texlive-amsmath \
    texlive-amsfonts \
    texlive-tools \
    texlive-graphics \
    texlive-subfig \
    texlive-titlesec \
    texlive-natbib \
    texlive-url \
    texlive-cleveref \
    texlive-placeins \
    \
    # ---- 数学字体 ----
    texlive-tex-gyre \
    texlive-tex-gyre-math \
    texlive-stix2-otf \
    \
    # ---- 中文字体 ----
    adobe-source-han-sans-cn-fonts \
    adobe-source-han-serif-cn-fonts \
    google-noto-sans-cjk-fonts \
    \
    # ---- Python 3 + pip（图表生成） ----
    python3 \
    python3-pip \
    \
    && dnf clean all

# ============================================================
#  Python 依赖（不依赖源码，利用 Docker 层缓存）
# ============================================================
RUN pip3 install --no-cache-dir matplotlib numpy

# ============================================================
#  先复制图表生成脚本和输出目录（仅脚本变更才重建此层）
# ============================================================
WORKDIR /workspace
COPY scripts/ scripts/
COPY figures/ figures/

# ============================================================
#  生成示例图表
# ============================================================
RUN python3 scripts/generate_figures.py

# ============================================================
#  复制其余源码（章节、表格、参考文献等）
#  放在最后，使其上方的 pip install / 图表生成 层可被缓存
# ============================================================
COPY . /workspace/

# ============================================================
#  编译论文：xelatex × 3 + bibtex
# ============================================================
RUN set -e; \
    echo "=== Pass 1: xelatex ==="; \
    xelatex -interaction=nonstopmode main.tex || true; \
    echo "=== Pass 2: bibtex ==="; \
    bibtex main || true; \
    echo "=== Pass 3: xelatex ==="; \
    xelatex -interaction=nonstopmode main.tex || true; \
    echo "=== Pass 4: xelatex ==="; \
    xelatex -interaction=nonstopmode main.tex || true; \
    echo "=== Checking output ==="; \
    ls -lh main.pdf; \
    test -f main.pdf && echo "=== BUILD SUCCESS ==="

# ============================================================
#  默认：复制 PDF 到挂载的工作目录
# ============================================================
CMD ["bash", "-c", "cp main.pdf /workdir/ && echo 'PDF -> main.pdf'"]
