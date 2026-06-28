import pymem
import pymem.process
import psutil
import numpy as np
import time
from typing import Optional, List, Tuple
import logging
from .offsets import Offsets

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, process_name: str = "DELTARUNE.exe"):
        self.process_name = process_name
        self.pm: Optional[pymem.Pymem] = None
        self.process_id: Optional[int] = None
        self.module_base: Optional[int] = None
        self.pointer_cache = {}

    def attach(self) -> bool:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and proc.info['name'].lower() == self.process_name.lower():
                    self.process_id = proc.info['pid']
                    break
            if not self.process_id:
                raise Exception("Process not found")
            self.pm = pymem.Pymem(self.process_id)
            module = pymem.process.module_from_name(self.pm.process_handle, self.process_name)
            self.module_base = module.lpBaseOfDll
            logger.info(f"Attached to {self.process_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to attach: {e}")
            return False

    def is_attached(self) -> bool:
        try:
            if self.pm and self.process_id:
                psutil.Process(self.process_id).status()
                return True
        except:
            pass
        return False

    def read_int(self, address: int) -> int:
        return self.pm.read_int(address)

    def write_int(self, address: int, value: int):
        self.pm.write_int(address, value)

    def close(self):
        if self.pm:
            self.pm.close_process()
