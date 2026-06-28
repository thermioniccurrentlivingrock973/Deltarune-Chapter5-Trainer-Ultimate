import pytest
from src.memory import MemoryManager

def test_memory_attach_not_running():
    mgr = MemoryManager("nonexistent_game_process.exe")
    assert not mgr.attach()
