# MVC Pattern in Modern Frontend Applications — Companion Code

MVC triad for React and Vue. Source:
<https://stackpractices.com/patterns/mvc-pattern-frontend/>

## Files

| File | Language | What it shows |
| --- | --- | --- |
| `UserModel.ts` | TypeScript | Pure Model: filter and sort logic with no framework imports |
| `UserController.ts` | TypeScript | Controller: fetch, search and sort orchestration over the Model |
| `UserListView.tsx` | React | Thin View that forwards events to the Controller and re-renders |
| `userMVC.ts` | TypeScript | Model + Controller in one module, for the Vue example |
| `UserListView.vue` | Vue | Same triad, Vue `<script setup>` version |

## Use

Drop `UserModel.ts`, `UserController.ts` and `UserListView.tsx` into a React +
TypeScript project. The Controller fetches `/api/users`, so point it at a real
endpoint or a mock (MSW, json-server) for local runs.

For Vue, copy `userMVC.ts` and `UserListView.vue`. The split versions
(`UserModel.ts` + `UserController.ts`) work too — just fix the import path.
