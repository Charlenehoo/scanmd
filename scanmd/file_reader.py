"""文件读取。"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


class FileReader:
    """把磁盘文件读成字符串，区分「不存在」和「读不了」。

    依次尝试多个编码，全部失败才算 unreadable。
    编码列表默认从 encodings.json 读，读不到就用内置兜底。
    """

    OK = "ok"
    MISSING = "missing"
    UNREADABLE = "unreadable"

    DEFAULT_ENCODINGS = ("utf-8", "utf-8-sig", "gbk")

    def __init__(self, encodings: tuple[str, ...] | None = None) -> None:
        self._encodings = encodings or self.DEFAULT_ENCODINGS

    @classmethod
    def from_json(cls, path: Path) -> "FileReader":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(f"[scan] config not found: {path}", file=sys.stderr)
            return cls()
        except json.JSONDecodeError as e:
            print(f"[scan] invalid JSON in {path}: {e}", file=sys.stderr)
            return cls()

        encodings = tuple(data.get("encodings", []))
        if not encodings:
            print(f"[scan] no encodings in {path}", file=sys.stderr)
            return cls()
        return cls(encodings)

    def read(self, path: str) -> tuple[str | None, str]:
        if not os.path.isfile(path):
            return None, self.MISSING

        try:
            data = Path(path).read_bytes()
        except OSError:
            return None, self.UNREADABLE

        if b"\x00" in data:
            return None, self.UNREADABLE

        for enc in self._encodings:
            try:
                return data.decode(enc), self.OK
            except UnicodeDecodeError:
                continue

        return None, self.UNREADABLE
