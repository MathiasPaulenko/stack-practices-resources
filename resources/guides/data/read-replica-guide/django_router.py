"""Django database router: reads to 'replica', writes and migrations to 'default'.

# settings.py
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


class ReadReplicaRouter:
    def db_for_read(self, model, **hints):
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"


# Usage: reads go to the replica, writes to the primary
# users = User.objects.filter(role='admin')            # replica
# user = User.objects.create(email='alice@example.com') # primary
