#!/usr/bin/env python3
"""
Tier 2 — 技能健康度离线扫描。

读取所有技能的 evolution 字段，应用纯规则分析，输出健康报告。
纯标准库实现，无 LLM 依赖。Haiku (L0) 执行。

用法:
  python scripts/check-skill-health.py skills/
  python scripts/check-skill-health.py skills/ --json
  python scripts/check-skill-health.py skills/ --skill delegation
"""

import os
import sys
import re
import json
from datetime import datetime

# Windows GBK console workaround
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_frontmatter(filepath):
    """Extract YAML frontmatter between --- markers. Returns raw text."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return ""
    parts = content.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def parse_evolution(frontmatter_text):
    """Parse evolution fields from frontmatter text."""
    result = {"usage_count": 0, "last_corrections": [], "stale_markers": []}

    # Extract evolution block
    match = re.search(r'evolution:\s*\n((?:\s+.*\n)*)', frontmatter_text)
    if not match:
        return result

    block = match.group(1)

    # usage_count
    uc = re.search(r'usage_count:\s*(\d+)', block)
    if uc:
        result["usage_count"] = int(uc.group(1))

    # last_corrections
    lc_section = re.search(r'last_corrections:\s*\n((?:\s+-\s+.*\n)*)', block)
    if lc_section:
        items = re.findall(r'-\s+"([^"]*)"', lc_section.group(1))
        result["last_corrections"] = items

    # stale_markers
    sm_section = re.search(r'stale_markers:\s*\n((?:\s+-\s+.*\n)*)', block)
    if sm_section:
        items = re.findall(r'-\s+"([^"]*)"', sm_section.group(1))
        result["stale_markers"] = items

    return result


def assess_skill(name, evolution, skill_path):
    """Apply health rules. Returns list of markers."""
    markers = []
    uc = evolution["usage_count"]
    corrections = evolution["last_corrections"]
    stales = evolution["stale_markers"]

    # Rule 1: High usage + corrections → needs review
    if uc > 10 and len(corrections) > 0:
        markers.append({
            "skill": name,
            "level": "review",
            "reason": f"高频使用 ({uc}次) 但有 {len(corrections)} 条纠正记录",
            "detail": corrections,
        })

    # Rule 2: Stale markers exist → content possibly outdated
    if stales:
        markers.append({
            "skill": name,
            "level": "stale",
            "reason": f"有 {len(stales)} 个疑似过时标记",
            "detail": stales,
        })

    # Rule 3: High usage + zero corrections → quality signal
    if uc > 20 and len(corrections) == 0 and not stales:
        markers.append({
            "skill": name,
            "level": "healthy",
            "reason": f"高频使用 ({uc}次)，零纠正，零过时标记",
            "detail": [],
        })

    # Rule 4: Zero usage → unused
    if uc == 0:
        markers.append({
            "skill": name,
            "level": "dormant",
            "reason": "从未被使用过",
            "detail": [],
        })

    # Rule 5: Corrections > usage/2 → high correction ratio
    if uc > 0 and len(corrections) > uc / 2:
        markers.append({
            "skill": name,
            "level": "unstable",
            "reason": f"纠正率过高 ({len(corrections)}/{uc} ≈ {len(corrections)/uc*100:.0f}%)",
            "detail": corrections,
        })

    return markers


def scan_skills(skills_dir, target_skill=None):
    """Scan all skill directories and return health report."""
    all_markers = []
    skill_summaries = []

    for item in os.listdir(skills_dir):
        skill_dir = os.path.join(skills_dir, item)
        if not os.path.isdir(skill_dir):
            continue

        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_md):
            continue

        if target_skill and item != target_skill:
            continue

        frontmatter = parse_frontmatter(skill_md)
        evolution = parse_evolution(frontmatter)
        markers = assess_skill(item, evolution, skill_dir)

        if markers:
            all_markers.extend(markers)

        skill_summaries.append({
            "name": item,
            "usage_count": evolution["usage_count"],
            "correction_count": len(evolution["last_corrections"]),
            "stale_count": len(evolution["stale_markers"]),
        })

    return skill_summaries, all_markers


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Tier 2 — 技能健康度离线扫描")
    parser.add_argument("skills_dir", help="skills/ 目录路径")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    parser.add_argument("--skill", help="仅检查指定技能")
    args = parser.parse_args()

    summaries, markers = scan_skills(args.skills_dir, args.skill)

    if args.json:
        print(json.dumps({
            "scan_time": datetime.now().isoformat(),
            "skills_scanned": len(summaries),
            "summaries": summaries,
            "markers": {m["level"]: [x for x in markers if x["level"] == m["level"]]
                       for m in markers}
        }, ensure_ascii=False, indent=2))
        return

    # Human-readable output
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"=== 技能健康报告 ({now}) ===")
    print(f"扫描技能数: {len(summaries)}\n")

    # Summary table
    print(f"{'技能':<25} {'使用':>5} {'纠正':>5} {'过时':>5}")
    print("-" * 42)
    for s in summaries:
        print(f"{s['name']:<25} {s['usage_count']:>5} {s['correction_count']:>5} {s['stale_count']:>5}")

    if not markers:
        print("\n[OK] 无异常标记，所有技能健康。")
        return

    # Group markers by level
    for level, label in [
        ("unstable", "[FAIL] 不稳定"),
        ("stale", "[WARN] 疑似过时"),
        ("review", "[WARN] 建议复核"),
        ("dormant", "[INFO] 从未使用"),
        ("healthy", "[OK] 健康"),
    ]:
        ms = [m for m in markers if m["level"] == level]
        if not ms:
            continue
        print(f"\n--- {label} ---")
        for m in ms:
            print(f"  [{m['skill']}] {m['reason']}")
            if m["detail"]:
                for d in m["detail"]:
                    print(f"    - {d}")

    # Action suggestions
    review_needed = [m for m in markers if m["level"] in ("unstable", "stale", "review")]
    if review_needed:
        print(f"\n---")
        print(f"建议复查 {len(review_needed)} 项。运行以下命令生成改进建议:")
        for m in review_needed[:3]:
            print(f"  # {m['skill']}: {m['reason']}")

    dormant = [m for m in markers if m["level"] == "dormant"]
    if dormant:
        print(f"\n{dormant[0]['skill']} 等 {len(dormant)} 个技能从未使用，考虑标记为 draft 或 deprecated。")


if __name__ == "__main__":
    main()
