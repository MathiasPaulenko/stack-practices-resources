# Generar Reportes PDF en Python — Recursos Companion

Ejemplos ejecutables para la receta [Generar Reportes PDF en Python](https://stackpractices.com/es/recipes/generate-pdf-report-python/).

## Archivos

| Archivo                 | Descripción                                               |
| ----------------------- | --------------------------------------------------------- |
| `basic_fpdf2.py`        | PDF de texto simple con fpdf2                             |
| `styled_reportlab.py`   | Tabla con estilo y título con ReportLab                   |
| `pdf_from_dataframe.py` | Renderizar un DataFrame de pandas a PDF                   |
| `header_footer.py`      | Números de página y texto de pie con ReportLab            |
| `chart_report.py`       | Embeber un gráfico de matplotlib en un PDF                |
| `weasyprint_html.py`    | Convertir HTML y CSS a PDF con WeasyPrint                 |
| `batch_invoices.py`     | Generar múltiples PDFs desde una lista de registros       |
| `requirements.txt`      | Dependencias de Python                                    |
| `README.md`             | Instrucciones en inglés                                   |
| `README.es.md`          | Instrucciones en español                                  |

## Inicio Rápido

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python basic_fpdf2.py
python styled_reportlab.py
python pdf_from_dataframe.py
python header_footer.py
python chart_report.py
python weasyprint_html.py
python batch_invoices.py
```

## Notas

- fpdf2 es ideal para PDFs de texto simples.
- ReportLab es mejor para tablas, encabezados, pies de página y reportes multi-página con estilo.
- WeasyPrint es el camino más fácil cuando el reporte ya existe como HTML y CSS.
