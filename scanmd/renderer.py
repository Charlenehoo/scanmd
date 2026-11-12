"""渲染。"""

from __future__ import annotations

from .report import Report


class MarkdownRenderer:
    """把 (路径, 语言, 内容) 渲染成一个 markdown 片段。"""

    def render(self, path: str, lang: str, content: str) -> str:
        body = content.rstrip("\n")
        return f"# {path}\n```{lang}\n{body}\n```\n\n"

    def render_skipped(self, report: Report) -> str:
        """把被跳过的文件渲染成 markdown section。无跳过时返回空串。"""
        if not (report.ignored or report.missing or report.unreadable):
            return ""

        parts = [
            "# Skipped files\n",
            "The following paths were given to scanmd but are **not** included above.\n",
        ]

        if report.ignored:
            parts.append(f"## Ignored by .scanignore ({len(report.ignored)})\n")
            parts.extend(f"- `{s}`" for s in report.ignored)
            parts.append("")

        if report.missing:
            parts.append(f"## Missing ({len(report.missing)})\n")
            parts.extend(f"- `{s}`" for s in report.missing)
            parts.append("")

        if report.unreadable:
            parts.append(f"## Unreadable ({len(report.unreadable)})\n")
            parts.extend(f"- `{s}`" for s in report.unreadable)
            parts.append("")

        return "\n".join(parts) + "\n"
