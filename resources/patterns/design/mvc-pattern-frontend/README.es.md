# Patrón MVC en Aplicaciones Frontend Modernas — Código complementario

Tríada MVC para React y Vue. Fuente:
<https://stackpractices.com/es/patterns/mvc-pattern-frontend/>

## Archivos

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `UserModel.ts` | TypeScript | Model puro: lógica de filtrado y ordenación sin imports de framework |
| `UserController.ts` | TypeScript | Controller: orquestación de fetch, búsqueda y ordenación sobre el Model |
| `UserListView.tsx` | React | View delgada que reenvía eventos al Controller y se re-renderiza |
| `userMVC.ts` | TypeScript | Model + Controller en un solo módulo, para el ejemplo de Vue |
| `UserListView.vue` | Vue | La misma tríada, versión Vue `<script setup>` |

## Uso

Copia `UserModel.ts`, `UserController.ts` y `UserListView.tsx` en un proyecto
React + TypeScript. El Controller pide `/api/users`, así que apúntalo a un
endpoint real o a un mock (MSW, json-server) para pruebas locales.

Para Vue, copia `userMVC.ts` y `UserListView.vue`. Las versiones separadas
(`UserModel.ts` + `UserController.ts`) también valen — solo corrige el import.
