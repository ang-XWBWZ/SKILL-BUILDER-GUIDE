# Phase 2: SCAN — 代码扫描详细方法

## 扫描原则

- **执行者**: Haiku (L0) — 必须下放，机械扫描无需推理
- **输入**: Phase 1 的技能规划 + 目标项目路径
- **输出**: 结构化扫描报告，含各层代码样本

## 扫描 Prompt 模板

```
Agent(
  description: "扫描{层名}代码样本",
  model: "haiku",
  prompt: """
    【任务】扫描 {project_path} 中 {layer_name} 的代码文件，提取关键模式
    【文件】{file_patterns}
    【扫描维度】
      {dimension_list}
    【输出格式】
      Conclusion: 该层共 {N} 个文件，主流模式为 {pattern}
      Basis:
        - 文件列表: [...]
        - 关键模式: [{具体的代码片段或结构描述}]
        - 异常情况: [{与主流模式不同的文件及原因}]
      Uncertainty: {扫描盲区或需要主模型确认的假设}
  """
)
```

## 接口层扫描

### 文件匹配
- Java: `**/controller/**/*.java`, `**/api/**/*.java`
- Python: `**/api/**/*.py`, `**/views/**/*.py`
- TypeScript: `**/routes/**/*.ts`, `**/controllers/**/*.ts`

### 扫描维度

| 维度 | 扫描内容 | 记录格式 |
|------|---------|----------|
| 路由声明 | 路由注册方式 | `{注解/装饰器/配置文件/函数}` |
| 参数校验 | 校验机制 | `{装饰器/中间件/手动校验/无}` |
| 响应封装 | 统一响应结构 | `{类名/函数名/无统一封装}` |
| 错误处理 | 错误处理方式 | `{全局异常处理/逐方法try-catch/无}` |
| API文档 | 文档生成方式 | `{Swagger/OpenAPI/无}` |

### 输出示例

```
Conclusion: 接口层共 12 个文件，使用 @RestController 注解，统一响应封装为 Result<T>
Basis:
  - 路由声明: @RequestMapping + @GetMapping/@PostMapping
  - 参数校验: @Valid + @NotNull/@NotBlank
  - 响应封装: Result<T> { code, message, data }
  - 错误处理: @ControllerAdvice 全局异常处理
  - 入口文件: src/main/java/com/example/controller/
Uncertainty: 未检查 Filter/Interceptor 层的参数预处理逻辑
```

## 业务层扫描

### 文件匹配
- Java: `**/service/**/*.java`, `**/manager/**/*.java`
- Python: `**/services/**/*.py`, `**/business/**/*.py`
- TypeScript: `**/services/**/*.ts`, `**/use-cases/**/*.ts`

### 扫描维度

| 维度 | 扫描内容 | 记录格式 |
|------|---------|----------|
| 抽象接口 | 是否有接口定义 | `{接口名列表/无}` |
| 一致性管理 | 事务声明方式 | `{@Transactional/手动/框架托管/无}` |
| 参数转换 | 模型转换方式 | `{Converter/MapStruct/手动new/无}` |
| 外部编排 | 跨服务调用 | `{Feign/RestTemplate/gRPC/无}` |

## 数据层扫描

### 文件匹配
- Java: `**/repository/**/*.java`, `**/dao/**/*.java`, `**/mapper/**/*.java`
- Python: `**/repositories/**/*.py`, `**/models/**/*.py`
- TypeScript: `**/repositories/**/*.ts`, `**/models/**/*.ts`

### 扫描维度

| 维度 | 扫描内容 | 记录格式 |
|------|---------|----------|
| 持久化方式 | ORM/查询方式 | `{JPA/MyBatis/Prisma/SQLAlchemy/原始SQL}` |
| 查询组织 | 查询存放方式 | `{方法命名查询/@Query注解/XML文件/内联}` |
| 分页方式 | 分页实现 | `{Pageable/PageHelper/手动limit/无}` |
| 数据源 | 数据源配置 | `{单数据源/多数据源/读写分离}` |

## 集成层扫描

### 扫描维度

| 维度 | 扫描内容 | 记录格式 |
|------|---------|----------|
| 远程调用 | 服务间通信 | `{Feign/RestTemplate/gRPC/无}` |
| 消息队列 | MQ组件 | `{Kafka/RabbitMQ/RocketMQ/无}` |
| 定时任务 | 调度方式 | `{@Scheduled/XXL-Job/Cron/无}` |
| 第三方SDK | 外部集成 | `{OSS/SMS/Payment/...}` |
