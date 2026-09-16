# Trigger Checks

## Should Trigger

| Request | Expected routing |
| --- | --- |
| `用受保护的亚马逊产品决策引擎分析这个证据包。` | Use the gateway; validate first and request transmission authorization before submission |
| `把这个 Amazon 产品立项 JSON 提交到私有决策服务并验证正式结果。` | Use the gateway; require endpoint, token, public key, and signed response |
| `Verify whether this saved result is an official engine response for my request.` | Use `inspect-response` and signature verification |

## Should Not Trigger

| Request | Expected routing |
| --- | --- |
| `只抓取这个 ASIN 的差评。` | Route to a review collection skill |
| `本地帮我算一下 FBA 利润，不要上传任何数据。` | Route to a local unit-economics workflow; do not use the gateway |
| `给这个产品生成 Amazon 主图。` | Route to an image workflow |

## Boundary Behavior

A general request for Amazon product analysis does not by itself authorize sending evidence to a private service. The gateway may prepare and validate the request, then must pause immediately before transmission and identify the destination and data categories.
