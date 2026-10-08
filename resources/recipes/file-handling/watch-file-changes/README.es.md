# Observar Cambios en Archivos — Ejemplos Companion

Watchers de sistema de archivos ejecutables en cuatro lenguajes, companion de la
[receta Observar Cambios en Archivos](https://stackpractices.com/es/recipes/watch-file-changes/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Qué muestra |
| --- | --- | --- |
| `debounced_watcher.py` | Python | handler de watchdog que coalesce los guardados rápidos del editor en un solo callback |
| `chokidar-watcher.js` | JavaScript | chokidar con filtros glob, debounce y `awaitWriteFinish` |
| `RecursiveWatcher.java` | Java | `WatchService` recursivo con thread pool, manejo de `OVERFLOW` y limpieza de claves inválidas |
| `watch.sh` | Bash | watcher con `inotifywait` y debounce simplificado (solo Linux) |

## Inicio rápido

```bash
# Python — requiere: pip install watchdog
python debounced_watcher.py ./src

# JavaScript — requiere: npm install chokidar
node chokidar-watcher.js ./src

# Java — JDK 7+
javac RecursiveWatcher.java && java RecursiveWatcher ./src

# Bash — solo Linux, requiere: apt install inotify-tools
./watch.sh ./src
```

## Advertencias

- `fs.watch` con `{ recursive: true }` necesita Node 20+ en Linux — usá chokidar para versiones viejas o consistencia multiplataforma.
- Los watchers nativos no pueden ver cambios en recursos de red (NFS/SMB) ni a través de bind mounts de contenedores; ahí usá polling (`usePolling: true` en chokidar, `FileAlterationMonitor` en Java).
- El debounce en bash usa un archivo de caché compartido — sirve para demos, no para uso concurrente en producción.
