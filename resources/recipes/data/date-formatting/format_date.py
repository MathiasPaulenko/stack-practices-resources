from datetime import datetime, timezone
from zoneinfo import ZoneInfo

now = datetime.now(timezone.utc)
print(now.isoformat())                          # 2026-06-10T14:30:00+00:00
print(now.strftime("%d/%m/%Y %H:%M %Z"))        # 10/06/2026 14:30 UTC
print(now.astimezone(ZoneInfo("Europe/Madrid")).strftime("%d/%m/%Y %H:%M %Z"))
