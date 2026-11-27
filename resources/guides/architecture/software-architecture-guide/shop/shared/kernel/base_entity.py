import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class BaseEntity:
    """Shared base for all domain entities. Lives in shared/kernel so every
    module can depend on it without depending on each other."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
