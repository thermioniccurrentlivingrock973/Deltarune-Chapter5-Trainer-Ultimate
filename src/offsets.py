from dataclasses import dataclass

@dataclass
class Offsets:
    base_address: int = 0x2A4B4B5
    hp_current: int = 0x28D
    hp_max: int = 0x291
    atk: int = 0x295
    def_: int = 0x299
    magic: int = 0x29D
    gold: int = 0x2B5
    inventory_ptr: int = 0x2D5
    battle_flag: int = 0x30D
    timer: int = 0x325
    items_base: int = 0x2A4B5A5

CURRENT_OFFSETS = Offsets()
