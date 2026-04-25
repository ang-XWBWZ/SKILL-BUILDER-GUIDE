#!/usr/bin/env python3
"""将技能目录打包为 .zip 存档，方便分发。"""

import zipfile
import os
import sys

def package_skill(skill_dir, output_dir="."):
    """Package a skill directory into a zip file."""
    skill_name = os.path.basename(skill_dir.rstrip("/\\"))
    zip_path = os.path.join(output_dir, f"{skill_name}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            for f in files:
                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, os.path.dirname(skill_dir))
                zf.write(full_path, arcname)

    print(f"打包完成: {zip_path}")

    # 列出内容
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            print(f"  {info.file_size:>8}  {info.filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python package-skill.py <skill_dir> [output_dir]")
        sys.exit(1)
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    package_skill(skill_dir, output_dir)
