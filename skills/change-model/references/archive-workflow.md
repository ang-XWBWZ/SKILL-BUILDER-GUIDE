# 存档流程与工具

> 对应 `SKILL-BUILDER-GUIDE.md` 第九章。此文件为 L3 参考。

## 两种工作流

### 手动存档（报告已写好）

```
编写报告 → 复核内容 → 执行存档命令 → 自动编号 → 更新索引
```

适用于：AI 会话中手动生成的结构化报告、已有变更文档需要归入统一索引。

### 自动存档（从 Git 生成）

```
指定 Git 范围 → 脚本分析 → 自动生成报告 → 自动编号 → 更新索引
```

适用于：已提交代码但未写报告，需要快速补全变更记录。

## 存档命令

```bash
# 将已有报告文件归档
python skills/change-model/scripts/archive-report.py \
  path/to/report.md \
  --title "新增筛选功能" \
  --type feature \
  --scope api

# 指定日期归档
python skills/change-model/scripts/archive-report.py \
  path/to/report.md \
  --title "重构支付" \
  --type refactor \
  --scope payment \
  --date 2026-04-27
```

## 存档校验清单

在报告进入最终存档前确认：

- [ ] 报告包含完整的四层结构（WHY / WHAT / HOW / VALIDATION）
- [ ] 调用链检查所有项目为 ✅
- [ ] 涉及的文件路径已与实际代码核对
- [ ] 回滚方案明确可执行
- [ ] 无敏感信息（密码、密钥、内部系统名 — 视项目而定）
- [ ] 变更标识 (`YYYYMMDD-NN`) 已分配
- [ ] INDEX.md 已更新（按时间 + 按类型双维度）

## 脚本说明

所有脚本为**参考实现**，需根据项目实际情况调整：
- 模板内容
- 路径约定（默认 `docs/changes/`）
- 评估规则（影响等级、风险项）
- 变更类型列表（feature/bugfix/refactor/config/other）

两个脚本均为纯 Python 标准库实现，无需安装依赖。
