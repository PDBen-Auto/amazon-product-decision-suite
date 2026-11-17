# Gateway de decisão de produto Amazon

`amazon-product-decision-gateway` · Português

## Objetivo e âmbito

Enviar um conjunto mínimo de provas a um motor privado alojado separadamente e verificar a resposta assinada. O cliente público não inclui o motor.

## Fundamento e dependências

Python 3.9+, cryptography, serviço HTTPS, token em variável de ambiente e chave pública Ed25519 de confiança. Operação, retenção e custos cabem ao fornecedor. Sem serviço, apenas preparação local.

## Entradas

Obrigatórios: decision_request JSON, produto, mercado, moeda e data. Um GO específico da empresa exige restrições comerciais. Autorização concreta do destino e dados; nunca guardar token em ficheiros.

## Saídas

request_validation.json; após autorização, decision_response.json e resumo. Verificar hashes do pedido/resultado, assinatura e versão; distinguir provas, modelos, lacunas e condições.

## Procedimento

1. Fixar âmbito/versão
2. retirar segredos, dados pessoais e caminhos internos
3. validar schema local
4. explicar destino/categorias e obter autorização específica
5. submeter e verificar hashes/assinatura
6. manter estado indisponível ou diagnóstico.

## Limites e condições de interrupção

Não reconstruir pesos privados nem inventar decisão local. Parar perante dados sensíveis, falta de permissão, assinatura/hash inválidos. Não seguir redirecionamentos com token. Exceção diagnóstica não é decisão oficial.

## Exemplo de pedido

Use `$amazon-product-decision-gateway` — Preparar provas de um suporte de telemóvel para os EUA e transmitir apenas após autorização para o serviço identificado; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Especificação completa

[Entrada do Skill e referências detalhadas](../../SKILL.md).

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

