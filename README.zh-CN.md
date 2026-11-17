# Amazon 产品私有决策网关

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

按用户明确指定的语言输出，否则跟随请求语言。保留命令、技能 ID、JSON 键、枚举值、单位和来源原文；翻译与原文分开，不通过语言推定国家、币种或司法辖区。先读取完整规范中与任务相关的详细引用，执行原有校验和授权要求。

## 安装与使用

下载或克隆仓库，将下列技能目录连同其 references、scripts、assets 等现有依赖一起放入宿主的技能目录。保留目录名和 SKILL.md；仅更换说明语言无需重复安装。安装命令供用户自行选择，不表示已安装或启用。

```sh
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git
```

## Amazon 产品私有决策网关

`amazon-product-decision-gateway`

将最小化证据包提交给独立部署的私有决策引擎并验证签名；公开客户端不包含引擎。

技能目录: `.`

**实现依据与依赖**

Python 3.9+、cryptography、HTTPS 服务、环境变量令牌与可信 Ed25519 公钥。服务部署、保留政策及费用由服务方提供；不可用时只准备本地请求。

**输入**

必需 decision_request JSON、产品、站点、币种、证据日期；公司专属 GO 需要业务约束。提交前需要确认具体目的地和传输范围；令牌不进文件。

**输出**

本地 request_validation.json；授权提交后生成 decision_response.json，核对请求/结果 hash、签名及引擎版本；摘要分开事实、模型值、缺口和条件。

[执行流程 · 边界与停止条件 · 示例请求](references/i18n/zh-CN.md)

> 请使用 `$amazon-product-decision-gateway` — 先准备美国站手机支架请求，获得指定服务传输授权后才提交并返回已验证结果；用简体中文输出，保留证据、未知项与操作边界。

## 语言覆盖与验证

这是本技能的本地化操作指南，覆盖用途、依赖、输入输出、步骤、示例及边界，不是全部引用文档的逐句翻译。详细技术引用、历史案例、脚本错误、示例网页及图片保留原文；助手可按请求解释它们。本次文档经过结构、链接和关键约束核对，尚无逐语种母语人工审校。

交付前逐项核对输入、证据、缺失值、输出文件和原有完成标准；未执行的步骤标为未验证，不把脚本退出成功当业务成功。
