# Amazon 产品决策套件概览

## 模块边界

公开 Gateway 通过稳定数据契约连接五个私有模块。以下内容描述职责和输入输出，不披露内部提示词、权重、阈值或公式。

| 私有模块 | 职责 | 主要输入 | 主要输出 |
| --- | --- | --- | --- |
| Decision Pipeline | 统一编排产品事实、市场、评价、权利、供应链、差异化、财务和阶段门 | 决策问题、证据包、业务约束 | 阶段矩阵、结论、条件、阻断、验证计划 |
| Evidence Contract | 将异构报告整理为可追溯证据对象 | 市场报告、评论、报价、政策来源 | `observed/calculated/modeled/inference/assumption` 记录 |
| Differentiation | 把客户问题转成可打样验证的产品定义 | VOC、竞品事实、约束 | 机制、规格、BOM 影响、实验和淘汰条件 |
| Supply Chain Feasibility | 判断规格、供应商、MOQ、模具、质量、合规和交期是否可执行 | 方案定义、报价、工艺和合规信息 | `PASS/CONDITIONAL/BLOCK`、阻断和补证要求 |
| Unit Economics & Cashflow | 判断完整利润和首单现金是否满足门槛 | 售价、费用、采购、物流、广告、退货、付款条件 | 贡献率、Break-even ACoS、情景和现金约束 |

## 与现有研究能力的关系

套件不替代市场 BI、评论采集、VOC、专利预筛或 Amazon 图片生产。它们负责采集和解释证据；决策套件负责统一数据口径、跨模块交接、阶段门和最终条件。

```text
市场 BI / 评论 / VOC / 专利 / 合规
                 |
                 v
          Evidence Contract
                 |
        +--------+--------+
        |                 |
Differentiation     Supply Chain
        |                 |
        +--------+--------+
                 |
       Unit Economics & Cash
                 |
          Decision Pipeline
```

图片工作流只在决策通过且用户明确请求时执行，不属于立项判断本身。

## 阶段门原则

- 市场吸引力不能覆盖安全、强制合规或权利阻断。
- 数值高分不能覆盖关键工艺不可实现。
- 假设和模型必须与观测事实区分。
- 缺少公司级利润和现金门槛时，不输出无条件 `GO`。
- 私有 Engine 不可用时，Gateway 不在本地模拟专有结论。
