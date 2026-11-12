# scanmd

把文件列表汇总成一个 markdown 文档,适合给 LLM 喂上下文。

读 stdin 的路径列表,按 `.scanignore` 跳过不需要的文件,把每个文件的内容
渲染成 `# path` + 代码块,输出到一个 markdown 文件。被跳过的路径会以
`# Skipped files` 段附在文档末尾,LLM 能知道上下文缺了什么。

## 安装

推荐用 [pipx](https://pipx.pypa.io/),命令全局可用,依赖隔离:

    pipx install scanmd

开发时想改代码立即生效:

    pipx install --editable /path/to/scanmd

也可以直接用 pip 装进当前环境:

    pip install scanmd

## 用法

    git ls-files | scanmd
    git ls-files | scanmd output.md

默认输出到 `scan.md`。不带管道直接跑会打印用法并以退出码 2 结束。

### 忽略规则

`.scanignore` 放在当前工作目录,按 `.gitignore` 子集语义跳过路径:

- 空行、`#` 开头的行忽略
- 模式不含 `/` 时,匹配路径中的任意一段
- 模式含 `/` 时,匹配完整相对路径
- 末尾 `/` 会被忽略
- 支持 `*` 通配符

示例:

    # 构建产物
    build/
    dist/

    # 文档图片
    *.png
    *.jpg

    # 第三方
    vendor/

### 编码回退

默认按 `utf-8` → `utf-8-sig` → `gbk` 顺序尝试解码,适配 Windows 中文环境。
含 NUL 字节的文件判定为二进制,跳过。想改编码列表,编辑安装包内的
`encodings.json`(editable 安装时直接改源码)。

### 输出

`scan.md` 末尾会附一段 `# Skipped files`,列出三类被跳过的路径:

- **Ignored by .scanignore**: 用户配置主动排除的
- **Missing**: 路径给了但文件不存在
- **Unreadable**: 二进制、编码全失败、或读不了

没有跳过时不输出这一段。

## 开发

    git clone https://github.com/Charlenehoo/scanmd.git
    cd scanmd
    python -m venv .venv
    .venv\Scripts\Activate.ps1      # Windows
    # source .venv/bin/activate     # Linux / macOS
    pip install -e .

也可以 `python -m scanmd` 直接跑。

## License

GPL-3.0-or-later
