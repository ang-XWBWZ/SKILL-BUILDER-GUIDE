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

## check-skill-health.py

Tier 2 离线扫描——读取所有技能的 `evolution` 字段，应用纯规则分析，输出健康报告。无需 LLM 调用，Haiku (L0) 执行。

```bash
# 扫描所有技能
python check-skill-health.py ../skills/

# JSON 输出
python check-skill-health.py ../skills/ --json

# 仅检查指定技能
python check-skill-health.py ../skills/ --skill delegation
```

## package-skill.py

将技能目录打包为 `.zip` 存档，用于分发或备份。

```bash
# 打包到当前目录
python package-skill.py ../skills/example-dev

# 打包到指定目录
python package-skill.py ../skills/example-dev ../dist/
```
