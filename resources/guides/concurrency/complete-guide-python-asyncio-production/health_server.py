# health_server.py — Health/liveness endpoints on a separate port.
from aiohttp import web


class HealthServer:
    """/health = readiness (deps), /live = process responds."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8081):
        self.healthy = True
        self.host = host
        self.port = port

    async def health_handler(self, request):
        if self.healthy:
            return web.json_response({"status": "healthy"})
        return web.json_response({"status": "unhealthy"}, status=503)

    async def liveness_handler(self, request):
        return web.json_response({"status": "alive"})

    async def start(self):
        app = web.Application()
        app.router.add_get("/health", self.health_handler)
        app.router.add_get("/live", self.liveness_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
