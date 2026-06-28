import asyncio
import logging
from typing import Dict, Optional
from discordrpc import DiscordRPC
from .memory import MemoryManager
from .offsets import CURRENT_OFFSETS
from .config import config

logger = logging.getLogger(__name__)

class Trainer:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.active_cheats: Dict[str, bool] = {
            "infinite_hp": False, "max_stats": False, "unlimited_items": False,
            "infinite_gold": False, "one_hit_kill": False, "speed_hack": False,
            "freeze_timer": False, "unlock_all": False,
        }
        self.loop_task: Optional[asyncio.Task] = None
        self.rpc: Optional[DiscordRPC] = None
        self.running = False

    async def start_loop(self):
        if self.running: return
        self.running = True
        logger.info("Trainer loop started.")
        self.loop_task = asyncio.create_task(self._cheat_loop())

    async def _cheat_loop(self):
        while self.running:
            if self.memory.is_attached():
                try:
                    base = self.memory.module_base
                    if self.active_cheats.get("infinite_hp"):
                        for i in range(3):
                            self.memory.write_int(base + CURRENT_OFFSETS.hp_current + (i * 0x4), 999)
                    if self.active_cheats.get("infinite_gold"):
                        self.memory.write_int(base + CURRENT_OFFSETS.gold, 9999999)
                except Exception as e:
                    logger.error(f"Cheat loop error: {e}")
                await asyncio.sleep(config.memory_scan_interval)
            else:
                await asyncio.sleep(2)

    async def stop_loop(self):
        self.running = False
        if self.loop_task: self.loop_task.cancel()
        logger.info("Trainer loop stopped.")

    def toggle_cheat(self, name: str, state: bool):
        if name in self.active_cheats:
            self.active_cheats[name] = state
            logger.info(f"Cheat '{name}' -> {state}")
