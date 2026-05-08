# Phase 3: GENERATE — 生成技能文件

## 生成规则

- **执行者**: Sonnet (L1)
- **输入**: Phase 1 技能规划 + Phase 2 扫描报告 + 匹配的模板
- **输出**: 技能文件。默认输出到 `.claude/skills/{name}/`（自动加载），模板/参考技能输出到 `skills/{name}/`（不自动加载）

### 输出路径选择

| 目标 | 输出路径 | 说明 |
|------|---------|------|
| 生产项目专属技能 | `.claude/skills/{name}/` | 自动加载 + `/skill` 命令 |
| 模板/参考技能 | `skills/{name}/` | 不自动加载，供方法论参考 |

## 生成 Prompt 模板

```
Agent(
  description: "生成{技能类型}技能文件",
  model: "sonnet",
  prompt: """
    【任务】为 {project_name} 生成专属的 {skill_type} 技能文件
    
    【技能规划】
    - 技能名: {skill_name}
    - 执行层: {model_tier}
    - 组合层: {skill_tier}
    - 创建理由: {reason}
    
    【代码扫描结果】
    {scan_results}
    
    【参照模板】
    {template_content}
    
    【生成要求】
    1. frontmatter 按 frontmatter-spec.md 填写完整（含双轴字段）
    2. 触发词从项目实际术语中提取（5-15个，覆盖操作类+询问类）
    3. 技术栈表填入扫描到的实际版本号（不得使用占位符）
    4. 代码示例使用扫描到的实际代码片段（脱敏后）
    5. 关联技能使用相对路径引用
    6. SKILL.md 正文 ≤ 5000 tokens
    7. openai.yaml 的 short_description 标注模型等级
    
    【输出格式】
    完整 SKILL.md 内容 + 完整 openai.yaml 内容
  """
)
```

## 各技能类型生成要点

### 规范技能 (dev)

- 技术栈表：填入 `package.json` / `pom.xml` / `requirements.txt` 中的实际版本
- 分层架构：根据扫描结果定制四层结构（项目可能只有三层或无集成层）
- 命名规范：从扫描样本中归纳实际命名模式，给出 3+ 个具体示例
- 兼容写法：记录扫描中发现的非主流写法及原因

### 代码地图 (code-map)

- 目录结构：使用 `find` / `tree` 输出，仅保留关键目录（≤3层深）
- 快速定位表：每个入口至少给出一个具体的文件匹配模式
- 路由映射表：从路由配置文件/注解中提取，列出实际路由
- 组件清单：列出 ≥80% 的顶层组件/模块

### 变更模型 (change-model)

- 调用链路模板：使用项目实际的层命名（如 Controller→Service→Repository）
- 风险等级定义：根据项目实际调整 L0-L3 的风险阈值
- 存档路径：确认 `docs/changes/` 在项目中是否已存在，如存在则沿用
- 示例：使用项目实际的一个简单变更作为填充示例

### 分治驱动 (delegation)

- L0 任务清单：根据项目技术栈扩充（如"查 Maven 依赖版本"）
- 下放格式：保持通用格式，增加项目特定的路径/配置示例

## 质量自检

生成完成后，在交付 Phase 4 验证之前，Sonnet 自检：

- [ ] 所有 `{placeholder}` 已替换为实际内容
- [ ] 技术栈版本号与扫描结果一致
- [ ] 文件路径引用使用项目实际路径
- [ ] 触发词不包含泛化词（如"开发"、"修改"），而是项目特定术语
- [ ] 双轴字段 (model_tier, skill_tier) 已填写
- [ ] context_budget 字段已填写
- [ ] 关联技能路径正确（相对路径，指向存在的目录）
