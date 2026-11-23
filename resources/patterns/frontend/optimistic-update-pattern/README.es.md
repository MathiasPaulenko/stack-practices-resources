# Patrón Optimistic Update

Compañero ejecutable del [patrón Optimistic Update](https://stackpractices.com/es/patterns/optimistic-update-pattern/): snapshot → UI optimista → petición → reconciliación o rollback, en React plano, React 19 y React Query.

## Contenido

- `LikeButton.jsx` — optimistic update mínimo: corazón lleno al instante, rollback ante error
- `TodoList.jsx` — alta/baja/toggle optimistas con IDs temporales y estilo `pending`
- `OptimisticTodo.jsx` — `useOptimistic` nativo de React 19 dentro de una transición (sin rollback manual)
- `useOptimisticTodo.js` — la misma lista con TanStack Query: snapshot en `onMutate`, rollback en `onError`, refetch en `onSettled`
- `useOptimisticState.js` — hook genérico de estado optimista para versiones anteriores a React 19
- `CommentEditor.jsx` — uso de `useOptimisticState`: borrador local, guardado optimista
- `EditableTitle.jsx` — manejo de conflictos con `version` y respuestas `409`
- `MixedOptimistic.jsx` — optimista para acciones de bajo riesgo, pesimista para quitar del carrito
- `BatchOptimistic.jsx` — update optimista en lote con rollback como unidad
- `package.json` — React 19 + TanStack Query

## Notas

- Toma el snapshot *antes* de mutar — el rollback solo es tan bueno como lo que capturaste.
- Los ítems nuevos llevan ID temporal (`crypto.randomUUID()`); cámbialo por el del servidor cuando llegue la respuesta.
- En React 19 prefiere el `useOptimistic` nativo; el `useOptimisticState` custom existe para versiones viejas.
- Los ejemplos llaman a endpoints `/api/...` — conéctalos a tu backend o a un mock (MSW) para ejecutarlos.
