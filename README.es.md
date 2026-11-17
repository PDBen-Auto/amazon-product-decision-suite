# Pasarela de decisión de producto Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

## Instalación y uso

Descarga o clona el repositorio y copia el directorio del Skill indicado, con sus references, scripts, assets y demás dependencias existentes, al directorio de Skills del entorno. Conserva el nombre y SKILL.md. Cambiar el idioma de la documentación no requiere otra instalación. Los comandos son opciones, no pruebas de instalación ni activación.

```sh
git clone https://github.com/PDBen-Auto/amazon-product-decision-suite.git
```

## Pasarela de decisión de producto Amazon

`amazon-product-decision-gateway`

Enviar pruebas minimizadas a un motor privado alojado por separado y verificar su respuesta firmada. El cliente público no contiene el motor.

Directorio del Skill: `.`

**Fundamento y dependencias**

Python 3.9+, cryptography, servicio HTTPS, token en variable de entorno y clave pública Ed25519 de confianza. Operación, conservación y costes corresponden al proveedor. Sin servicio solo se prepara la solicitud local.

**Entradas**

Obligatorios: decision_request JSON, producto, mercado, moneda y fecha. Un GO empresarial exige restricciones del negocio. Hace falta autorización específica del destino y datos enviados; el token nunca va en archivos.

**Salidas**

request_validation.json; tras autorización, decision_response.json y resumen. Verificar hashes de solicitud/resultado, firma y versión; separar hechos, modelos, carencias y condiciones.

[Procedimiento · Límites y condiciones de parada · Ejemplo de solicitud](references/i18n/es.md)

> Usa `$amazon-product-decision-gateway` — Preparar pruebas de un soporte de teléfono para EE.UU. y enviarlas solo después de autorizar la transmisión al servicio identificado; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.
