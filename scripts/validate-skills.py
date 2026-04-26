#!/usr/bin/env python3
"""验证技能文件的准确性：文件路径存在性、引用完整性、frontmatter 完整性。"""

import os
import sys
import yaml  # requires: pip install pyyaml

def validate_skill(skill_dir):
    """Validate a single skill directory."""
    errors = []
    warnings = []
    skill_name = os.path.basename(skill_dir)

    # 1. 检查必需文件
    required_files = ["SKILL.md", "agents/openai.yaml"]
    for f in required_files:
        path = os.path.join(skill_dir, f)
        if not os.path.exists(path):
            errors.append(f"缺少必需文件: {f}")

    # 2. 检查 SKILL.md frontmatter
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()
        # 检查 frontmatter 分隔符
        if not content.startswith("---"):
            errors.append("SKILL.md: 缺少 frontmatter 起始分隔符 ---")
        # 检查必要字段
        if "name:" not in content[:500]:
            errors.append("SKILL.md: 缺少 name 字段")
        # 检查状态字段
        if "status:" in content[:500]:
            status_match = None
            for line in content[:500].split("\n"):
                if line.strip().startswith("status:"):
                    status_match = line.strip()
                    break
            if status_match:
                status_value = status_match.split(":", 1)[1].strip()
                valid_statuses = ["draft", "active", "deprecated", "superseded"]
                if status_value not in valid_statuses:
                    warnings.append(f"SKILL.md: status 值 '{status_value}' 无效，有效值: {', '.join(valid_statuses)}")
                if status_value == "superseded" and "supersededBy:" not in content[:500]:
                    warnings.append("SKILL.md: status 为 superseded 但缺少 supersededBy 字段")
        else:
            warnings.append("SKILL.md: 建议添加 status 字段 (draft|active|deprecated|superseded)")

        # 检查 reviewBy 是否过期
        if "reviewBy:" in content[:500]:
            from datetime import datetime
            for line in content[:500].split("\n"):
                if line.strip().startswith("reviewBy:"):
                    date_str = line.strip().split(":", 1)[1].strip()
                    try:
                        review_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        if review_date < datetime.now().date():
                            warnings.append(f"SKILL.md: reviewBy ({date_str}) 已过期，建议复核技能内容")
                    except ValueError:
                        warnings.append(f"SKILL.md: reviewBy 日期格式无效，应为 YYYY-MM-DD")

    # 3. 检查 openai.yaml
    yaml_path = os.path.join(skill_dir, "agents/openai.yaml")
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not data:
                errors.append("agents/openai.yaml: 文件为空或格式错误")
            else:
                # 检查 triggers
                triggers = data.get("triggers", [])
                if len(triggers) < 5:
                    warnings.append(f"agents/openai.yaml: triggers 仅 {len(triggers)} 个，建议至少 5 个")
                if len(triggers) > 15:
                    warnings.append(f"agents/openai.yaml: triggers 达 {len(triggers)} 个，建议不超过 15 个")
                # 检查模型等级标注
                desc = data.get("interface", {}).get("short_description", "")
                if not any(tag in desc for tag in ["L0", "L1", "L2", "L3"]):
                    warnings.append("agents/openai.yaml: short_description 未标注模型等级 (L0/L1/L2/L3)")
        except yaml.YAMLError as e:
            errors.append(f"agents/openai.yaml: YAML 解析错误: {e}")

    return skill_name, errors, warnings


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"=== 技能验证报告 ===")
    print(f"扫描目录: {os.path.abspath(root)}\n")

    total_skills = 0
    all_errors = []
    all_warnings = []

    for item in os.listdir(root):
        skill_dir = os.path.join(root, item)
        if not os.path.isdir(skill_dir):
            continue
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_md):
            continue  # 不是技能目录

        total_skills += 1
        name, errors, warnings = validate_skill(skill_dir)
        status = "[OK]" if not errors else "[FAIL]"
        print(f"\n{status} {name}")
        for e in errors:
            print(f"  错误: {e}")
            all_errors.append(f"{name}: {e}")
        for w in warnings:
            print(f"  警告: {w}")
            all_warnings.append(f"{name}: {w}")

    print(f"\n--- 摘要 ---")
    print(f"扫描技能数: {total_skills}")
    print(f"错误数: {len(all_errors)}")
    print(f"警告数: {len(all_warnings)}")

    if all_errors:
        print("\n[FAIL] 验证未通过，请修复上述错误。")
        sys.exit(1)
    elif all_warnings:
        print("\n⚠️ 验证通过但存在警告。")
    else:
        print("\n[OK] 全部通过！")

if __name__ == "__main__":
    main()
