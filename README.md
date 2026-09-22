# Amazon Product Decision Suite

[English](README.en.md) | 中文

[![Release](https://img.shields.io/github/v/release/PDBen-Auto/amazon-product-decision-suite?display_name=tag)](https://github.com/PDBen-Auto/amazon-product-decision-suite/releases)
[![Validate](https://github.com/PDBen-Auto/amazon-product-decision-suite/actions/workflows/validate.yml/badge.svg)](https://github.com/PDBen-Auto/amazon-product-decision-suite/actions/workflows/validate.yml)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111111)](SKILL.md)
[![skills.sh](https://skills.sh/b/PDBen-Auto/amazon-product-decision-suite)](https://skills.sh/PDBen-Auto/amazon-product-decision-suite/amazon-product-decision-gateway)
[![License](https://img.shields.io/badge/license-source--available-59636e?style=flat-square)](LICENSE)

**Amazon FBA product research、product validation 与 Go/No-Go 决策 Skill。** 面向产品经理、Amazon Seller、跨境电商品类负责人和 Private Label 团队，覆盖市场研究、Voice of Customer、产品差异化、供应链可行性、单位经济与首单现金约束。

面向 Amazon 实物产品立项的证据驱动决策系统。它不是再生成一份“市场看起来不错”的研究报告，而是帮助产品经理把市场、用户、产品、供应链和财务证据组织成可执行、可追溯、可否决的立项结论。

公开仓库提供一个可安装的 Codex Gateway Skill，用统一数据契约连接市场 BI、评论/VOC、专利与合规、差异化研发、供应链和单位经济分析，同时把核心决策方法保留在独立私有 Engine 中。

> 当前公开版本是 Gateway，而不是私有决策 Engine。它可以在本地完成数据校验、敏感信息检查、请求哈希和官方结果验签；要返回正式产品决策，还需要部署私有服务。

## 产品经理面对的真正问题

产品经理通常不缺报告，缺的是一条能经得住复盘的决策链。市场工具说有需求、评论工具说有痛点、专利工具提示风险、供应商说可以生产、利润表说可能赚钱，但这些结论往往来自不同时间、不同口径和不同假设，最后仍然没人能明确回答“是否值得立项”。

这套系统面向 Amazon 产品经理、品类负责人、选品负责人、供应链负责人和小型品牌创始人，重点解决五个问题：

- 证据来自哪里，属于事实、计算、模型还是假设？
- 差异化能否变成可打样的规格、工艺和验证实验？
- MOQ、模具、质量、合规、包装和交期是否可行？
- 广告、退货、头程、关税和现金周期计入后是否仍然赚钱？
- 哪些问题必须阻断，哪些问题允许带条件进入下一阶段？

最终输出不是泛泛的机会描述，而是 `GO / CONDITIONAL_GO / NO_GO / INSUFFICIENT_EVIDENCE`、阶段状态矩阵、条件、阻断、证据缺口和下一轮验证计划。

## 常见 Skill 如何解决问题

| Skill 类型 | 它擅长解决什么 | 通常停在哪里 |
| --- | --- | --- |
| 市场 BI / 选品研究 | 市场规模、趋势、价格带、竞争强度和关键词机会 | 能说明“市场是否有吸引力”，不能单独证明产品可做、可赚或适合公司 |
| 评论采集 / VOC | 收集用户原话、聚类痛点、识别使用场景和抱怨主题 | 能说明“用户哪里不满意”，但不会自动形成规格、BOM、打样实验和退出条件 |
| 专利 / Design-around | 预筛外观专利、权利风险和可绕开的设计空间 | 能提示风险与设计边界，不能完成供应链、利润和最终立项判断 |
| 供应商 / 成本工具 | 比较报价、MOQ、模具、交期和部分成本 | 容易把供应商口径当成事实，且常与市场证据和退货/广告风险脱节 |
| 利润计算器 | 计算毛利、贡献率、Break-even ACoS 或情景结果 | 计算本身清楚，但输入假设未必有证据，也不处理合规、权利和工艺硬阻断 |
| 通用产品分析框架 | 提供 SWOT、定位、机会或战略讨论 | 适合思考和沟通，但往往缺少机器可校验的数据契约和可执行阶段门 |
| Amazon 图片工作流 | 生成概念图、主图、A+ 和 Listing 素材 | 属于产品定义之后的生产环节，不应该替代立项决策 |

## 这套 Skill 的差异化优势

它并不是在每一个单点任务上替代专业 Skill。只抓评论、只做市场 BI、只查专利时，原有单点工具通常更直接；它的优势出现在“必须做出跨职能产品决策”的场景。

1. **从研究结果推进到决策结果**：把市场吸引力、用户问题、产品方案、制造可行性和公司财务门槛放进同一条阶段门流程。
2. **统一证据口径**：明确区分 `observed`、`calculated`、`modeled`、`inference` 和 `assumption`，避免把推测包装成事实。
3. **把差异化变成研发任务**：差异化方案必须落到产品机制、规格变化、BOM/工艺影响、验证实验、通过阈值和淘汰条件。
4. **硬阻断优先于综合高分**：安全、强制合规、权利或关键工艺问题可以直接阻断项目，不允许被市场热度或平均分掩盖。
5. **判断公司适配性，而不只判断市场好坏**：将目标贡献率、广告、退货、MOQ、首单现金和回本约束纳入结论；好市场不等于适合当前公司。
6. **跨 Skill 交接可审计**：每个结论能回到证据 ID、数据日期、来源、计算或假设，减少团队在市场、产品、采购和财务之间反复对口径。
7. **保护方法，同时验证官方结果**：核心权重、阈值和方法留在私有 Engine；公开 Gateway 负责最小化数据、绑定请求哈希并验证服务器签名。

从产品管理角度看，核心价值不是“分析更多”，而是更早暴露错误假设、把下一步验证说清楚，并减少一个看起来有机会但最终无法生产、无法盈利或无法合规的产品被错误立项。

## 典型使用场景

- **Amazon FBA Product Research / 亚马逊选品立项**：把市场规模、价格带、竞争、评论和产品事实汇总为是否继续投入的正式判断。
- **Product Validation / 新品验证**：识别最危险的假设，明确进入打样、询盘、小批量测试前必须补齐的证据。
- **Voice of Customer to Product Differentiation**：把评论痛点转成机制、规格、BOM/工艺影响、实验与淘汰条件。
- **Supplier Sourcing / Supply Chain Feasibility**：判断 MOQ、模具、关键工艺、质量、合规、包装、交期和供应商承诺是否可执行。
- **Unit Economics / Profitability / Cash Flow**：将采购、物流、Amazon 费用、广告、退货、贡献率、Break-even ACoS 和首单现金放进同一决策。
- **Stage-Gate / Go-No-Go Decision**：为产品经理、品类负责人、供应链和财务提供统一的结论、条件、阻断和下一轮验证计划。

它适合跨多个证据源做正式立项、比较多个产品概念，或需要向管理层解释为什么进入或停止一个项目。

它不适合只抓评论、只生成图片、只查一个专利、没有私有 Engine 却要求本地猜测官方评分，或把输出当作法律、认证、采购和量产批准。

常见检索语义：`Amazon product research`、`Amazon FBA product validation`、`product opportunity analysis`、`new product development`、`product manager decision support`、`voice of customer`、`supplier sourcing`、`supply chain feasibility`、`unit economics`、`go/no-go decision`、`Codex Skill`、`Agent Skills`。

## 公开架构

```text
研究证据与业务约束
        |
        v
Amazon Product Decision Gateway  <-- 本仓库
  - 数据最小化与敏感信息检查
  - 请求契约校验
  - 确认外部处理授权
  - 请求 SHA-256 绑定
        |
        | HTTPS + 短期令牌
        v
Private Decision Engine           <-- 不公开
  - 统一编排与阶段门
  - 证据冲突处理
  - 差异化研发方法
  - 供应链可行性
  - 单位经济与现金流
  - 版本化结果签名
        |
        v
Gateway 校验结果哈希与 Ed25519 签名
```

完整模块边界见 [套件概览](docs/SUITE_OVERVIEW.zh-CN.md) 和 [系统架构](docs/ARCHITECTURE.md)。

## 公开内容

- 可安装的 `amazon-product-decision-gateway` Skill
- 请求与响应 JSON 契约
- 本地校验、脱敏检查、哈希和 HTTPS 客户端
- Ed25519 官方结果验签
- 合成测试数据、单元测试和 GitHub Actions
- 公开边界扫描和发布完整性清单
- 提示词中立的作者溯源与发布签名

## 不公开内容

- 私有 Engine 的提示词、内部编排与模型配置
- 证据置信度和冲突处理启发式
- 阶段门权重、阈值和淘汰规则
- 差异化评分、供应商评估和询盘方法
- 单位经济计算器的专有政策与内部假设
- 真实产品案例、供应商资料、生产数据、令牌和签名私钥

公开边界不是代码混淆。核心方法从未交付到不可信客户端，官方结果使用服务器签名确认来源。

## 安装

### 一条命令安装

```bash
npx skills add PDBen-Auto/amazon-product-decision-suite --skill amazon-product-decision-gateway
```

将仓库克隆到 Codex Skill 目录，并保持仓库根目录中的 `SKILL.md`、`agents/`、`scripts/` 和 `references/` 相邻：

```bash
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git ~/.codex/skills/amazon-product-decision-gateway
cd ~/.codex/skills/amazon-product-decision-gateway
python -m pip install -r requirements.txt
```

也可以从 [GitHub Releases](https://github.com/PDBen-Auto/amazon-product-decision-suite/releases) 下载官方签名版本，并解压到同一目录。

## 本地验证

无需私有服务即可运行：

```bash
python scripts/decision_client.py validate tests/fixtures/valid_request.json
python -m unittest discover -s tests -v
python scripts/check_public_boundary.py .
python scripts/build_release_manifest.py . --check
python scripts/release_provenance.py verify-release \
  --manifest PUBLIC_MANIFEST.sha256 \
  --provenance RELEASE_PROVENANCE.json \
  --signature RELEASE_PROVENANCE.sig \
  --public-key PUBLISHER_PUBLIC_KEY.pem
```

示例数据完全为合成数据。不要把客户资料、供应商联系人、Amazon 账户数据或真实请求包提交到公开 Issue。

## 连接私有 Engine

正式提交前在仓库之外配置：

```text
AMAZON_DECISION_API_URL=https://your-private-service.example/v1/decisions
AMAZON_DECISION_API_TOKEN=<short-lived-scoped-token>
AMAZON_DECISION_PUBLIC_KEY=/trusted/path/engine-result-public-key.pem
```

Gateway 只接受 HTTPS，不跟随携带令牌的重定向，并要求用户在提交前明确确认外部处理。部署要求见 [私有 Engine 部署说明](docs/PRIVATE_ENGINE_DEPLOYMENT.md)。

## 输出

私有 Engine 的正式响应应包含：

- `GO / CONDITIONAL_GO / NO_GO / INSUFFICIENT_EVIDENCE`
- 阶段状态矩阵
- 置信度、条件、阻断和证据缺口
- 下一轮验证计划
- Engine 版本、请求哈希、结果哈希和 Ed25519 签名

Gateway 不会在本地重建或猜测私有评分。当 Engine 不可用时，只返回经过校验的请求包和明确的不可用状态。

## 发布溯源

公开版本包含 `.well-known/skill-provenance.json`、`PUBLISHER_PUBLIC_KEY.pem`、`PUBLIC_MANIFEST.sha256`、`RELEASE_PROVENANCE.json` 和 `RELEASE_PROVENANCE.sig`。

作者公钥 SHA-256 指纹：

```text
d64d7ebc963fdaa86a44573bd226e8bb135d9d95818c5f39df88e0a45e886596
```

来源记录不写入 `SKILL.md` 或 `agents/openai.yaml`，不会改变 AI 行为，也不包含遥测或回传。它只是辅助线索，真正的发布证明来自签名、GitHub 历史和受信任指纹。详见 [发布溯源](docs/provenance.md)。

## 项目状态

- Gateway 数据契约、敏感信息检查、哈希绑定和验签已实现。
- 合成请求、异常输入、HTTPS 限制、授权要求和签名流程均有测试。
- 私有 Engine、令牌服务、数据保留政策和生产监控不包含在本仓库中。
- 在私有服务未部署前，本仓库不能独立生成正式 `GO / NO_GO` 决策。

## 安全与贡献

- 安全问题请按 [SECURITY.md](SECURITY.md) 私密报告。
- 贡献范围和 Pull Request 要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 不要在 Issue、PR、Actions 日志或测试夹具中提交真实业务数据和凭据。

## 许可证

本仓库公开可见，但当前许可证不是 OSI 开源许可证。它允许检查和使用未修改的官方发布，不授予修改、衍生、再分发或冒充官方版本的权利。正式商业使用前请阅读 [LICENSE](LICENSE) 并由专业法律顾问审阅。

## Related PDBen-Auto Skills

- [Amazon Review Intelligence](https://github.com/PDBen-Auto/amazon-review-intelligence-skill) — written-review collection and VOC analysis.
- [SellerSprite Amazon Market Research BI](https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill) — keyword-to-ASIN discovery and auditable category BI.
- [Design Patent Search And Design Around](https://github.com/PDBen-Auto/design-patent-design-around-skill) — design-rights pre-screening and redesign planning.
