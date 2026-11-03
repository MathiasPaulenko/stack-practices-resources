import json
import logging
import time
from datetime import datetime

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_api_call(self, request: Request, response, user_id: str | None):
        self.logger.info(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "user_id": user_id,
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent", ""),
            "api_key": request.headers.get("x-api-key", "")[:8] + "..." if request.headers.get("x-api-key") else None,
            "response_time_ms": getattr(request.state, "response_time", None)
        }))
    
    def log_security_event(self, event: str, details: dict):
        self.logger.warning(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details
        }))

audit = AuditLogger()

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed_ms = (time.time() - start) * 1000
    
    request.state.response_time = round(elapsed_ms, 2)
    
    # Get user from JWT if present
    user_id = None
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            payload = jwt_service.verify_token(auth_header[7:])
            user_id = payload["sub"]
        except Exception:
            pass
    
    audit.log_api_call(request, response, user_id)
    
    # Log suspicious activity
    if response.status_code == 401:
        audit.log_security_event("auth_failure", {
            "ip": request.client.host,
            "path": request.url.path,
            "method": request.method
        })
    elif response.status_code == 403:
        audit.log_security_event("access_denied", {
            "ip": request.client.host,
            "path": request.url.path,
            "user_id": user_id
        })
    
    return response
