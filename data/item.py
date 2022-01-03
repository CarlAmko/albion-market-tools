from dataclasses import dataclass


@dataclass()
class ItemStack:
	id: str
	quantity: int
