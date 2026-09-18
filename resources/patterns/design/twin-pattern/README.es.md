# Patrón Twin — Código complementario

Versiones ejecutables de las implementaciones del Patrón Twin del recurso
[Patrón Twin](https://stackpractices.com/es/patterns/twin-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `twin_widget.py` | `Widget` en Python + twins `Graphic`/`Interactive` con referencias mutuas, chequeo fail-fast para twins sin vincular, y una suite `unittest` que cubre delegación, aislamiento de twin con stub e intercambio de twins |
| `twin-widget.ts` | Versión en TypeScript con una interfaz `WidgetLike` para poder testear los twins contra stubs |

## Requisitos

- Python 3.10+ (usa `typing.Protocol`; sin dependencias externas)
- TypeScript: `npx tsx twin-widget.ts` o compila con `tsc`

## Notas

- La referencia de vuelta se conecta en el constructor de `Widget`, así
  que un twin nunca puede quedar sin vincular — los guardas
  `linked()`/`_linked()` lanzan un error claro si creas un twin a mano y
  olvidas `twin.widget = w`.
- `WidgetLike` es la superficie mínima que un twin lee (`name`, `x`, `y`,
  `width`, `height`). Inyectar esa interfaz en lugar del `Widget`
  concreto es lo que hace que los twins sean testeables con un stub.
- En lenguajes con recolector de basura el ciclo Widget ↔ twin es
  inofensivo. En C++/Rust usa una referencia de vuelta débil
  (`weak_ptr`, `Rc<Weak>`).
