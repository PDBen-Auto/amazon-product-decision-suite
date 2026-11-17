# Pasarela de decisión de producto Amazon

`amazon-product-decision-gateway` · Español

## Objetivo y alcance

Enviar pruebas minimizadas a un motor privado alojado por separado y verificar su respuesta firmada. El cliente público no contiene el motor.

## Fundamento y dependencias

Python 3.9+, cryptography, servicio HTTPS, token en variable de entorno y clave pública Ed25519 de confianza. Operación, conservación y costes corresponden al proveedor. Sin servicio solo se prepara la solicitud local.

## Entradas

Obligatorios: decision_request JSON, producto, mercado, moneda y fecha. Un GO empresarial exige restricciones del negocio. Hace falta autorización específica del destino y datos enviados; el token nunca va en archivos.

## Salidas

request_validation.json; tras autorización, decision_response.json y resumen. Verificar hashes de solicitud/resultado, firma y versión; separar hechos, modelos, carencias y condiciones.

## Procedimiento

1. Fijar alcance y versión
2. eliminar secretos, datos personales y rutas internas
3. validar schema local
4. explicar destino y categorías y obtener permiso concreto
5. enviar y verificar hashes/firma
6. conservar estado no disponible o diagnóstico.

## Límites y condiciones de parada

No reconstruir pesos privados ni inventar un dictamen local. Detener por datos sensibles, falta de permiso, firma/hash inválidos. No seguir redirecciones con token. Una excepción diagnóstica no es una decisión oficial.

## Ejemplo de solicitud

Usa `$amazon-product-decision-gateway` — Preparar pruebas de un soporte de teléfono para EE.UU. y enviarlas solo después de autorizar la transmisión al servicio identificado; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Especificación completa

[Entrada del Skill y referencias detalladas](../../SKILL.md).

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

