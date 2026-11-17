# Gateway de decisão de produto Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

## Instalação e utilização

Transfira ou clone o repositório e copie o diretório do Skill indicado, com as suas references, scripts, assets e demais dependências existentes, para o diretório de Skills do ambiente. Preserve o nome e SKILL.md. Mudar o idioma da documentação não exige outra instalação. Os comandos são opções, não provas de instalação ou ativação.

```sh
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git
```

## Gateway de decisão de produto Amazon

`amazon-product-decision-gateway`

Enviar um conjunto mínimo de provas a um motor privado alojado separadamente e verificar a resposta assinada. O cliente público não inclui o motor.

Diretório do Skill: `.`

**Fundamento e dependências**

Python 3.9+, cryptography, serviço HTTPS, token em variável de ambiente e chave pública Ed25519 de confiança. Operação, retenção e custos cabem ao fornecedor. Sem serviço, apenas preparação local.

**Entradas**

Obrigatórios: decision_request JSON, produto, mercado, moeda e data. Um GO específico da empresa exige restrições comerciais. Autorização concreta do destino e dados; nunca guardar token em ficheiros.

**Saídas**

request_validation.json; após autorização, decision_response.json e resumo. Verificar hashes do pedido/resultado, assinatura e versão; distinguir provas, modelos, lacunas e condições.

[Procedimento · Limites e condições de interrupção · Exemplo de pedido](references/i18n/pt.md)

> Use `$amazon-product-decision-gateway` — Preparar provas de um suporte de telemóvel para os EUA e transmitir apenas após autorização para o serviço identificado; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.
