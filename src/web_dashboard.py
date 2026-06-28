from aiohttp import web
import json
from .trainer import Trainer

class WebDashboard:
    def __init__(self, trainer: Trainer, port: int = 4200):
        self.trainer = trainer
        self.port = port
        self.app = web.Application()
        self.websockets = set()
        self.app.router.add_get("/", self.index)

    async def index(self, request):
        return web.Response(text="<h1>Trainer Dashboard Running</h1>", content_type="text/html")

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", self.port)
        await site.start()
