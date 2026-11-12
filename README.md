# scanmd

把文件列表汇总成一个 markdown 文档,适合给 LLM 喂上下文。

## 安装

    pip install -e .

## 用法

    git ls-files | scanmd
    git ls-files | scanmd output.md

默认输出到 `scan.md`。`.scanignore` 按 `.gitignore` 子集语义跳过路径。

## License

GPL-3.0-or-later
