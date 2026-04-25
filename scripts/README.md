# Scripts — 工具脚本

## validate-skills.py

验证技能目录的完整性：必需文件存在性、frontmatter 格式、YAML 解析、模型等级标注。

```bash
# 验证所有技能
python validate-skills.py ../skills/

# 验证单个技能
python validate-skills.py ../skills/example-dev
```

依赖：`pip install pyyaml`

## package-skill.py

将技能目录打包为 `.zip` 存档，用于分发或备份。

```bash
# 打包到当前目录
python package-skill.py ../skills/example-dev

# 打包到指定目录
python package-skill.py ../skills/example-dev ../dist/
```
