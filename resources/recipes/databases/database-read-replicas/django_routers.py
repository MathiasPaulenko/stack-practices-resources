"""Django database router for read replica splitting.

Add to settings.py:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'app',
            'HOST': 'master.db.internal',
            'PORT': '5432',
        },
        'replica': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'app',
            'HOST': 'replica1.db.internal',
            'PORT': '5432',
        },
    }
    DATABASE_ROUTERS = ['myapp.routers.ReadReplicaRouter']
"""

import random


class ReadReplicaRouter:
    """Route reads to replica, writes to default (primary)."""

    def db_for_read(self, model, **hints):
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"


class RoundRobinReplicaRouter:
    """Round-robin across multiple replicas.

    Configure multiple replica databases as 'replica_0', 'replica_1', etc.
    """

    REPLICA_COUNT = 2

    def __init__(self):
        self._counter = 0

    def db_for_read(self, model, **hints):
        db = f"replica_{self._counter % self.REPLICA_COUNT}"
        self._counter += 1
        return db

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
