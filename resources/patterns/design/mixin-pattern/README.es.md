# Patrón Mixin — Código complementario

Versiones ejecutables de las implementaciones del Patrón Mixin del recurso
[Patrón Mixin](https://stackpractices.com/es/patterns/mixin-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `mixins.py` | `SerializableMixin` + `TimestampMixin` en Python compuestos en `User` mediante herencia múltiple cooperativa, más una suite `unittest` que testea el mixin contra un host desechable y documenta el MRO |
| `mixins.ts` | Mixins tipados en TypeScript (`Loggable`, `Serializable`, `Validatable`) como funciones que envuelven una clase base — `EnhancedUser` conserva cada método mezclado con tipado completo |

## Requisitos

- Python 3.10+ (solo stdlib)
- TypeScript: `npx tsx mixins.ts` o compilar con `tsc`

## Notas

- El `super().__init__(*args, **kwargs)` cooperativo en cada mixin de Python es lo que mantiene viva la cadena del MRO. Quítalo y toda clase a su derecha en `class User(TimestampMixin, SerializableMixin)` nunca se inicializa — silenciosamente.
- `User.__mro__` es `User → TimestampMixin → SerializableMixin → object`, así que el mixin más a la izquierda gana cualquier conflicto de nombres. El orden es semántica, no estilo.
- En TypeScript el orden de los mixins funciona igual a nivel de tipos: `Loggable(Serializable(Validatable(User)))` produce una clase compuesta distinta de cualquier otra permutación.
- Para mixins estilo `Object.assign` en JavaScript, recordá que los getters se evalúan una vez al copiar — usa `Object.getOwnPropertyDescriptors` + `Object.defineProperties` para preservarlos.
