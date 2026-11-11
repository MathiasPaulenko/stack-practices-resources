# Factory Pattern — Code Examples

Runnable examples for the [Factory Pattern article](https://stackpractices.com/patterns/factory-pattern/) on StackPractices.

Two examples per language:

1. **Notification factory** — the canonical shape: a product interface, concrete products, and a registry-based factory. New channels are added with `register()` instead of editing the factory.
2. **Database connection factory** — a production-style variant where products carry their own configuration and a `Map` of creators routes the request. The same structure behind driver loading and plugin systems.

## Files

| Language | Canonical | Applied |
| --- | --- | --- |
| Python | `python/notification_factory.py` | `python/database_factory.py` |
| JavaScript | `javascript/notification_factory.js` | `javascript/database_factory.js` |
| Java | `java/NotificationFactory.java` | `java/DatabaseFactory.java` |

## Run

```bash
python python/notification_factory.py
python python/database_factory.py

node javascript/notification_factory.js
node javascript/database_factory.js

javac java/NotificationFactory.java java/DatabaseFactory.java
java -cp java NotificationFactory
java -cp java DatabaseFactory
```

Every example runs standalone with no third-party dependencies.
