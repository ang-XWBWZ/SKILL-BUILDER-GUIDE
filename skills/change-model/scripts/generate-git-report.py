#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参考实现 — 从 Git 历史分析生成结构化变更报告。

⚠️ 需根据项目实际情况调整：
  - 报告模板中的项目名称 / 技术栈
  - 影响评估的判别规则（assess_impact 函数）
  - 风险等级定义（assess_risk 函数）
  - 默认输出路径
  - 报告四层模板的具体章节内容

依赖：仅 Python 标准库。需在 git 仓库内执行。

用法:
  python generate-git-report.py --range "HEAD~3..HEAD" --title "新增筛选功能" --archive
  python generate-git-report.py --range "main..feature-x" --title "重构支付模块" --type refactor
  python generate-git-report.py --range "HEAD~1..HEAD" --title "修复登录bug" --type bugfix --output report.md
"""

import subprocess
import sys
import os
import re
import json
import argparse
from datetime import datetime


# --------------------------------------------------------------------------
# Git 数据提取
# --------------------------------------------------------------------------

def run_git(cmd, cwd=None):
    """执行 git 命令并返回 stdout。"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=cwd, timeout=30
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"[ERROR] 超时: {cmd}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[ERROR] 执行失败: {cmd} — {e}", file=sys.stderr)
        return ""


def parse_git_log(range_spec):
    """提取提交列表。

    返回 list[dict]，每个 dict: {hash, author, date, message}
    """
    fmt = "%H|%an|%ai|%s"
    output = run_git(f'git log {range_spec} --format="{fmt}" --no-merges')
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) >= 4:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3],
            })
        elif len(parts) >= 2:
            commits.append({
                "hash": parts[0],
                "author": parts[1] if len(parts) > 1 else "",
                "date": "",
                "message": parts[-1],
            })

    return commits


def parse_git_diff(range_spec):
    """提取变更文件列表和统计信息。

    返回:
      files: list[dict] — {status, path} status: A=新增 M=修改 D=删除
      additions: int
      deletions: int
      diff_raw: str — 完整 diff 内容
    """
    # --name-status: 文件级变更
    ns_output = run_git(f'git diff --name-status {range_spec}')
    files = []
    if ns_output:
        for line in ns_output.split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) == 2:
                status, path = parts
                label = {"A": "新增", "M": "修改", "D": "删除", "R": "重命名"}.get(status[0], status)
                files.append({"status": status, "label": label, "path": path})

    # --shortstat: 行数统计
    ss_output = run_git(f'git diff --shortstat {range_spec}')
    additions, deletions = 0, 0
    if ss_output:
        m_add = re.search(r'(\d+)\s+insertion', ss_output)
        m_del = re.search(r'(\d+)\s+deletion', ss_output)
        additions = int(m_add.group(1)) if m_add else 0
        deletions = int(m_del.group(1)) if m_del else 0

    # 完整 diff（限制 5000 行为参考上限，避免报告过大）
    diff_raw = run_git(f'git diff {range_spec}')
    diff_lines = diff_raw.split("\n")
    if len(diff_lines) > 5000:
        diff_raw = "\n".join(diff_lines[:5000]) + f"\n\n... (截断，共 {len(diff_lines)} 行)"

    return files, additions, deletions, diff_raw


def current_branch():
    """获取当前分支名。"""
    return run_git("git rev-parse --abbrev-ref HEAD") or "unknown"


def parse_range_files(range_spec):
    """列出范围内变更涉及的文件（仅路径）。"""
    output = run_git(f'git diff --name-only {range_spec}')
    if not output:
        return []
    return [p.strip() for p in output.split("\n") if p.strip()]


# --------------------------------------------------------------------------
# 影响与风险评估（通用规则 — 按项目实际情况调整）
# --------------------------------------------------------------------------

def assess_impact_level(file_count, additions, deletions):
    """根据变更规模评估影响等级。

    L0: <3 文件，<50 行变更 → 无外部影响
    L1: 3-10 文件，或 50-200 行 → 内部变更
    L2: >10 文件，或 >200 行 → 外部契约变更
    L3: 涉及数据/配置迁移 → 需制定迁移方案（本函数无法自动判断，默认回 L1/L2）
    """
    total_churn = additions + deletions
    if file_count < 3 and total_churn < 50:
        return "L0 — 无外部影响"
    elif file_count <= 10 and total_churn <= 200:
        return "L1 — 内部变更"
    else:
        return "L2 — 外部契约变更（需人工确认是否为 L3）"


def assess_risk_items(files, additions, deletions):
    """自动生成基础风险项列表。"""
    risks = []
    # 按文件变更类型评估
    new_count = sum(1 for f in files if f["status"] == "A")
    mod_count = sum(1 for f in files if f["status"] == "M")
    del_count = sum(1 for f in files if f["status"] == "D")

    if new_count > 0:
        level = "L0" if new_count <= 2 else "L1"
        risks.append({
            "name": f"新增 {new_count} 个文件",
            "level": level,
            "desc": "新文件可能引入未测试的代码路径",
            "mitigation": "检查新文件的测试覆盖",
        })
    if mod_count > 0:
        level = "L0" if mod_count <= 5 else "L1"
        risks.append({
            "name": f"修改 {mod_count} 个文件",
            "level": level,
            "desc": "修改现有逻辑可能影响已有功能",
            "mitigation": "回归测试覆盖受影响模块",
        })
    if del_count > 0:
        risks.append({
            "name": f"删除 {del_count} 个文件",
            "level": "L1",
            "desc": "删除文件如存在残留引用将导致编译/运行时错误",
            "mitigation": "全局搜索引用并清理",
        })
    if additions + deletions > 500:
        risks.append({
            "name": "大范围变更",
            "level": "L2",
            "desc": f"共 {additions + deletions} 行变更，review 难度高",
            "mitigation": "分批提交、增强 Code Review",
        })
    return risks


# --------------------------------------------------------------------------
# 报告生成
# --------------------------------------------------------------------------

def build_report(title, change_type, scope, range_spec, commits, files,
                 additions, deletions, diff_raw):
    """按 change-model 四层架构生成报告 markdown。"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_id = now.strftime("%Y%m%d")
    branch = current_branch()
    file_count = len(files)
    impact_level = assess_impact_level(file_count, additions, deletions)
    risk_items = assess_risk_items(files, additions, deletions)

    # ---- 第一层：WHY ----
    why_section = f"""## 第一层：WHY — 变更背景与需求

### 1. 变更背景

| 要素 | 说明 |
|------|------|
| **需求来源** | Git 历史自动分析 |
| **分析范围** | `{range_spec}` |
| **分析分支** | `{branch}` |
| **提交数量** | {len(commits)} 个 |
| **分析时间** | {now.strftime('%Y-%m-%d %H:%M:%S')} |

### 2. 提交历史

| # | 提交 | 作者 | 日期 | 说明 |
|:-:|------|------|------|------|
"""

    for i, c in enumerate(commits, 1):
        short_hash = c["hash"][:8]
        why_section += f'| {i} | `{short_hash}` | {c["author"]} | {c["date"][:10]} | {c["message"]} |\n'

    # ---- 第二层：WHAT ----
    what_section = f"""## 第二层：WHAT — 影响与风险

### 3. 影响分析

#### 3.1 变更统计

| 类型 | 数量 |
|------|------|
| 新增文件 | {sum(1 for f in files if f["status"] == "A")} |
| 修改文件 | {sum(1 for f in files if f["status"] == "M")} |
| 删除文件 | {sum(1 for f in files if f["status"] == "D")} |
| 新增行数 | +{additions} |
| 删除行数 | -{deletions} |
| 净变更 | {additions - deletions:+d} |

#### 3.2 影响评估

| 维度 | 说明 |
|------|------|
| **影响等级** | {impact_level} |
| **涉及文件** | {file_count} 个 |
| **变更规模** | +{additions}/-{deletions} 行 |
| **分析范围** | `{range_spec}` |

### 4. 风险评估

| 风险项 | 级别 | 说明 | 缓解措施 |
|--------|:----:|------|----------|
"""

    if risk_items:
        for r in risk_items:
            what_section += f'| {r["name"]} | {r["level"]} | {r["desc"]} | {r["mitigation"]} |\n'
    else:
        what_section += "| 无显著风险 | L0 | 变更规模极小 | — |\n"

    # ---- 第三层：HOW ----
    how_section = f"""## 第三层：HOW — 设计与实现

### 5. 变更文件清单

| 序号 | 操作 | 文件路径 |
|:----:|:----:|----------|
"""

    for i, f in enumerate(files, 1):
        how_section += f'| {i} | {f["label"]} | `{f["path"]}` |\n'

    if diff_raw:
        how_section += f"""### 6. 代码变更详情

```diff
{diff_raw}
```
"""
    else:
        how_section += "\n> 无 diff 内容（范围可能为空或无变更）\n"

    # ---- 第四层：VALIDATION ----
    validation_section = f"""## 第四层：VALIDATION — 验证与交付

### 7. 调用链检查

> **注意**：本报告由 Git 历史自动生成，调用链检查需人工补充。请在测试前完成以下检查。

| 检查项 | 状态 | 说明 |
|--------|:----:|------|
| 入口验证 | ⬜ | 待人工检查 |
| 类型检查 | ⬜ | 待人工检查 |
| 最终调用 | ⬜ | 待人工检查 |
| 错误处理 | ⬜ | 待人工检查 |

### 8. 交付信息

| 项目 | 值 |
|------|-----|
| **分支** | `{branch}` |
| **分析范围** | `{range_spec}` |
| **生成时间** | {now.strftime('%Y-%m-%d %H:%M:%S')} |
| **涉及提交** | {len(commits)} 个 |
| **变更文件** | {file_count} 个 |

### 9. 回滚参考

回滚到 `{range_spec}` 范围之前的状态：

```bash
# 查看变更前的提交
git log {range_spec.split("..")[0] if ".." in range_spec else range_spec} -1 --oneline

# 回滚操作（请根据实际情况选择）
# git revert <commit-hash>...
```
"""

    report = f"""# {title} 变更报告

> **变更标识**: `{date_id}-XX`（归档时自动编号）
> **变更类型**: `{change_type}`
> **影响等级**: `{impact_level}`
> **分析范围**: `{range_spec}`

---

{why_section}
---

{what_section}
---

{how_section}
---

{validation_section}
---

*此报告由 `generate-git-report.py` 自动生成。调用链检查章节需人工补充。*

*报告时间: {now.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return report


# --------------------------------------------------------------------------
# 存档操作
# --------------------------------------------------------------------------

def slugify(text, max_len=40):
    """将文本转为安全的文件名片段。"""
    slug = re.sub(r'[^a-zA-Z0-9一-鿿\-]', '-', text)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:max_len]


def _append_index_entry(date_str, filename, title, change_type, scope):
    """在 docs/changes/INDEX.md 中追加一条记录。"""
    index_path = "docs/changes/INDEX.md"
    _ensure_index_exists()

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_row = f"| {date_str} | [{title}]({date_str}/{filename}) | {change_type} | `{scope}` | DONE |\n"

    # 插入到 "按时间排序" 表格末尾
    marker = "## 按类型排序"
    if marker in content:
        content = content.replace(marker, new_row + "\n" + marker)

    # 同时按类型追加
    type_markers = {
        "feature": "### 功能开发",
        "bugfix": "### Bug 修复",
        "refactor": "### 重构",
        "config": "### 配置变更",
    }
    type_marker = type_markers.get(change_type)
    if type_marker and type_marker in content:
        type_entry = f"- {date_str} [{title}]({date_str}/{filename}) — `{scope}`\n"
        content = content.replace(type_marker, type_marker + "\n" + type_entry)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def archive_report(report, title, change_type, scope):
    """将报告写入 docs/changes/ 并更新索引。"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_id = now.strftime("%Y%m%d")

    archive_dir = os.path.join("docs", "changes", date_str)
    os.makedirs(archive_dir, exist_ok=True)

    # 1. 先确保 INDEX.md 存在（报告文件写入前），避免重复条目
    _ensure_index_exists()

    # 2. 自动编号：统计当天已有报告数 + 1
    existing = [
        f for f in os.listdir(archive_dir)
        if f.endswith(".md") and f != "INDEX.md" and not f.startswith(".")
    ]
    seq = len(existing) + 1

    slug = slugify(title)
    filename = f"{date_id}-{seq:02d}-{slug}.md"
    filepath = os.path.join(archive_dir, filename)

    # 3. 更新报告中的标识
    report = report.replace(f"`{date_id}-XX`", f"`{date_id}-{seq:02d}`")

    # 4. 写入报告文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    # 5. 追加条目到 INDEX.md
    _append_index_entry(date_str, filename, title, change_type, scope)

    return filepath


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


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="从 Git 历史生成结构化变更报告（change-model 四层架构）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate-git-report.py --range "HEAD~3..HEAD" --title "新增筛选功能"
  python generate-git-report.py --range "main..feature-x" --title "重构支付" --type refactor --archive
  python generate-git-report.py --range "HEAD~1..HEAD" --title "修复bug" --type bugfix --output /tmp/report.md
        """,
    )
    parser.add_argument(
        "--range", default="HEAD~1..HEAD",
        help="Git 分析范围 (默认: HEAD~1..HEAD)"
    )
    parser.add_argument(
        "--title", required=True,
        help="报告标题"
    )
    parser.add_argument(
        "--type", default="feature",
        choices=["feature", "bugfix", "refactor", "config", "other"],
        help="变更类型 (默认: feature)"
    )
    parser.add_argument(
        "--scope", default="未指定",
        help="影响范围描述 (如: site/cms/api)"
    )
    parser.add_argument(
        "--archive", action="store_true",
        help="存档到 docs/changes/ 并更新 INDEX.md"
    )
    parser.add_argument(
        "--output",
        help="输出文件路径（默认输出到 stdout）"
    )

    args = parser.parse_args()

    # 检查是否在 git 仓库中
    if not os.path.isdir(".git"):
        print("[ERROR] 当前目录不是 git 仓库根目录，请在项目根目录执行此脚本。", file=sys.stderr)
        sys.exit(1)

    print(f"[分析] 范围: {args.range}")
    commits = parse_git_log(args.range)
    if not commits:
        print("[WARN] 未找到提交记录，范围可能为空。", file=sys.stderr)
    else:
        print(f"[分析] 找到 {len(commits)} 个提交")

    print("[分析] 提取 diff...")
    files, additions, deletions, diff_raw = parse_git_diff(args.range)
    print(f"[分析] {len(files)} 个文件变更, +{additions}/-{deletions} 行")

    report = build_report(
        title=args.title,
        change_type=args.type,
        scope=args.scope,
        range_spec=args.range,
        commits=commits,
        files=files,
        additions=additions,
        deletions=deletions,
        diff_raw=diff_raw,
    )

    if args.archive:
        filepath = archive_report(report, args.title, args.type, args.scope)
        print(f"\n[存档] 报告已生成: {filepath}")
    elif args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[输出] 报告已写入: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
