#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参考实现 — 将手动编写的变更报告存档到 docs/changes/。

⚠️ 需根据项目实际情况调整：
  - 存档目录结构（默认 docs/changes/YYYY-MM-DD/）
  - 报告命名规范（默认 YYYYMMDD-NN-slug.md）
  - INDEX.md 的路径和模板
  - 变更类型列表

依赖：仅 Python 标准库。

用法:
  python archive-report.py path/to/report.md --title "新增筛选功能"
  python archive-report.py path/to/report.md --title "重构支付" --type refactor
  python archive-report.py path/to/report.md --title "修复认证bug" --type bugfix --scope api
"""

import sys
import os
import re
import shutil
import argparse
from datetime import datetime


# --------------------------------------------------------------------------
# 工具函数
# --------------------------------------------------------------------------

def slugify(text, max_len=40):
    """将文本转为安全的文件名片段。"""
    slug = re.sub(r'[^a-zA-Z0-9一-鿿\-]', '-', text)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:max_len]


def read_report(filepath):
    """读取报告文件内容。"""
    if not os.path.exists(filepath):
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------
# 索引管理
# --------------------------------------------------------------------------

def _ensure_index_exists():
    """确保 INDEX.md 存在（不扫描已有文件，创建最小模板）。"""
    index_path = "docs/changes/INDEX.md"
    if os.path.exists(index_path):
        return
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("""# 变更索引

## 按时间排序

| 日期 | 报告 | 类型 | 范围 | 状态 |
|------|------|:----:|------|:----:|

## 按类型排序

### 功能开发

### Bug 修复

### 重构

### 配置变更
""")


def _append_index_entry(date_str, filename, title, change_type, scope):
    """追加一条记录到 INDEX.md。"""
    index_path = "docs/changes/INDEX.md"
    _ensure_index_exists()

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_row = f"| {date_str} | [{title}]({date_str}/{filename}) | {change_type} | `{scope}` | DONE |\n"

    marker = "## 按类型排序"
    if marker in content:
        content = content.replace(marker, new_row + "\n" + marker)

    # 同时按类型追加
    type_headers = {
        "feature":   "### 功能开发",
        "bugfix":    "### Bug 修复",
        "refactor":  "### 重构",
        "config":    "### 配置变更",
    }
    type_marker = type_headers.get(change_type)
    if type_marker and type_marker in content:
        type_entry = f"- {date_str} [{title}]({date_str}/{filename}) — `{scope}`\n"
        content = content.replace(type_marker, type_marker + "\n" + type_entry)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------
# 存档操作
# --------------------------------------------------------------------------

def archive(report_path, title, change_type, scope):
    """将报告复制到存档目录并更新索引。"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_id = now.strftime("%Y%m%d")

    archive_dir = os.path.join("docs", "changes", date_str)
    os.makedirs(archive_dir, exist_ok=True)

    # 1. 先确保 INDEX.md 存在（报告文件写入前），避免重复条目
    _ensure_index_exists()

    # 2. 自动编号
    existing = [
        f for f in os.listdir(archive_dir)
        if f.endswith(".md") and f != "INDEX.md" and not f.startswith(".")
    ]
    seq = len(existing) + 1

    slug = slugify(title)
    filename = f"{date_id}-{seq:02d}-{slug}.md"
    dest_path = os.path.join(archive_dir, filename)

    # 3. 复制报告（保留原始文件不变）
    shutil.copy2(report_path, dest_path)

    # 4. 更新索引
    _append_index_entry(date_str, filename, title, change_type, scope)

    print(f"[存档] {report_path} → {dest_path}")
    return dest_path


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="将手动编写的变更报告存档到 docs/changes/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python archive-report.py report.md --title "新增筛选功能"
  python archive-report.py path/to/report.md --title "重构支付" --type refactor --scope api
  python archive-report.py report.md --title "修复登录" --type bugfix
        """,
    )
    parser.add_argument(
        "report_file",
        help="报告文件路径"
    )
    parser.add_argument(
        "--title", required=True,
        help="报告标题（用于生成文件名和索引条目）"
    )
    parser.add_argument(
        "--type", default="feature",
        choices=["feature", "bugfix", "refactor", "config", "other"],
        help="变更类型 (默认: feature)"
    )
    parser.add_argument(
        "--scope", default="未指定",
        help="影响范围描述"
    )
    parser.add_argument(
        "--date",
        help="指定日期 YYYY-MM-DD（默认今天）"
    )

    args = parser.parse_args()

    # 读取报告确认可读
    content = read_report(args.report_file)
    print(f"[读取] {args.report_file} ({len(content)} 字符)")

    dest = archive(
        report_path=os.path.abspath(args.report_file),
        title=args.title,
        change_type=args.type,
        scope=args.scope,
    )

    print(f"\n完成: {os.path.abspath(dest)}")


if __name__ == "__main__":
    main()
