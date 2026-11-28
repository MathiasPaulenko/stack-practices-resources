# Plantilla de Diagramas de Sistema — Ejemplos C4

Recursos de la [Plantilla de Diagramas de Sistema](https://stackpractices.com/es/docs/system-diagram-template/): diagramas C4 de contexto y contenedores en Mermaid, un workspace en Structurizr DSL y un checklist de revisión.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `c4-context.mmd` | Diagrama de contexto C4 Nivel 1 en Mermaid |
| `c4-container.mmd` | Diagrama de contenedores C4 Nivel 2 en Mermaid |
| `workspace.dsl` | Workspace Structurizr DSL (vistas de contexto + contenedores) |
| `diagram-review-checklist.md` | Checklist de revisión previa al merge |

## Uso

Renderiza los archivos Mermaid con mermaid-cli:

```bash
mmdc -i c4-context.mmd -o context.svg
mmdc -i c4-container.mmd -o container.svg
```

O levanta Structurizr Lite para vistas C4 interactivas:

```bash
docker run -it --rm -p 8080:8080 -v "$PWD:/usr/local/structurizr" structurizr/lite
```

Commitea las fuentes de los diagramas (`.mmd`, `.dsl`) junto al documento — nunca solo la imagen renderizada.
