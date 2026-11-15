# Balanceo de carga — Código complementario

Implementaciones ejecutables de la receta [Distribuir Tráfico con Algoritmos de Load Balancing](https://stackpractices.com/es/recipes/load-balancing/) de StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `load_balancer.py` | Anillo de hash consistente con nodos virtuales: al retirar uno de tres nodos solo ~1/N de las claves se remapean, frente a casi todas con `hash % N` ingenuo. Además un round-robin ponderado suave que entrelaza las elecciones en lugar de producir ráfagas. Corre con Python 3 estándar. |
| `load-balancer.js` | Balanceador de menor tiempo de respuesta en Node.js: puntúa los backends por latencia media rodante más una penalización por conexión, descarga al servidor más rápido y deja de enrutar al que no está sano. |
| `SmoothWeightedBalancer.java` | El round-robin ponderado suave de Nginx en Java 17+: cuotas proporcionales exactas, secuencia entrelazada (compara con el orden por bloques con ráfagas). `javac` + `java`, sin dependencias. |

## Inicio rápido

```bash
python load_balancer.py
node load-balancer.js
javac SmoothWeightedBalancer.java && java SmoothWeightedBalancer
```

Salida esperada: el anillo remapea ~1/3 de las claves cuando un nodo sale
mientras `hash % N` remapea la mayoría; el selector de menor latencia
favorece al backend de 20 ms ~90 % de las veces y no da tráfico al muerto;
el selector ponderado produce una secuencia 5:3:1 entrelazada.

## Qué adaptar para producción

- La clave de enrutado del anillo es lo que identifique "mismo destino":
  ID de usuario, token de sesión, clave de caché — elige una que sobreviva
  reconexiones, no la IP del cliente (los móviles cambian de red a media
  sesión).
- El menor tiempo de respuesta real necesita health checks externos; la
  latencia por sí sola no distingue "lento" de "muerto". Combina
  `markUnhealthy` con una sonda activa tipo `GET /health`.
- El round-robin ponderado asume que los pesos reflejan capacidad.
  Vuelve a medir tras cambios de hardware y usa semántica de `slow_start`
  cuando un servidor se reincorpora para que las cachés frías no colapsen
  con una cuota completa.
- Estos son selectores del lado del cliente. Para balanceo de
  infraestructura, la receta cubre las configuraciones equivalentes en
  Nginx (`least_conn`, `weight`, `backup`, `keepalive`), HAProxy y DNS
  con Route 53.
