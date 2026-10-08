# Plantilla de Clasificación de Datos

Archivos complementarios de la [Plantilla de Clasificación de Datos](https://stackpractices.com/es/docs/data-classification-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `data-classification-template.md` | Plantilla rellenable: cuatro niveles, inventario de datasets, reglas de manejo, registro de excepciones |
| `data-classification-example.md` | Ejemplo completado para un SaaS B2B pequeño, con las decisiones no obvias documentadas |

## Uso

1. Copia `data-classification-template.md` a tu wiki o manual de seguridad.
2. Reemplaza los `<placeholders>` y rellena el inventario de datasets — exporta primero la lista de tus almacenes (RDS, S3, warehouses, herramientas SaaS) para no olvidar ninguno.
3. Usa `data-classification-example.md` como referencia del nivel de razonamiento que merece cada fila.
4. Conecta los niveles a la aplicación real: reglas DLP, políticas de bucket, checks de esquema en CI.
5. Revisa trimestralmente (Restringido), semestralmente (Confidencial), anualmente (Interno/Público).

Los cuatro niveles mapean a las decisiones que los ingenieros toman de verdad: ¿puedo poner esto en un ticket público? ¿Puedo enviarlo por email? ¿Necesita un flujo de aprobación?
