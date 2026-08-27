from typing import List, Optional

from .models import User


class UserService:
    def __init__(self, users: Optional[List[User]] = None):
        self._users = users or []

    def get_active_users(self) -> List[User]:
        return [user for user in self._users if user.can_login()]

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self._users:
            if user.email == email:
                return user
        return None

    def toggle_user_status(self, user_id: int) -> bool:
        for user in self._users:
            if user.id == user_id:
                user.is_active = not user.is_active
                return True
        return False
