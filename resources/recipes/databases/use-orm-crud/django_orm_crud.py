# Django ORM CRUD — drop these models into a Django app's models.py.
#
# Usage:
#   python manage.py makemigrations && python manage.py migrate
#   python manage.py shell < django_orm_crud.py   (functions section only)

from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default="user")

    class Meta:
        indexes = [models.Index(fields=["role"])]


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


def run_crud() -> None:
    """Execute inside `python manage.py shell` or a management command."""
    # Create
    user = User.objects.create(email="alice@example.com", role="admin")

    # Read with eager loading — prefetch_related avoids N+1 on the FK reverse
    users = User.objects.filter(role="admin").prefetch_related("posts")
    print("admins:", users.count())

    # Update
    user.role = "superadmin"
    user.save()

    # Bulk create
    User.objects.bulk_create(
        [User(email=f"user{i}@example.com") for i in range(100)]
    )

    # Bulk update
    User.objects.filter(role="user").update(role="member")

    # Aggregation
    from django.db.models import Count

    active = User.objects.annotate(post_count=Count("posts")).filter(post_count__gt=5)
    print("with >5 posts:", active.count())

    # Delete
    user.delete()
