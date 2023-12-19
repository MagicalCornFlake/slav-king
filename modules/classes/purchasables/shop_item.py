from modules import variables
from modules.classes.abstract import Clickable


class ShopItem(Clickable):
    def __init__(self, pos: tuple[int, int], name: str | int, cost: int):
        self.x_pos, self.y_pos = pos
        self.name = name
        self.cost = cost

    @property
    def affordable(self):
        return variables.money_count >= self.cost
