"""Definitions of abstract classes that other classes will inherit from."""

from modules import variables


class Clickable:
    """Abstract class for objects which will be hovered over or clicked by the user's mouse."""

    dimensions: list[int]

    def is_hovered(
        self, mouse_pos: tuple[int, int], dimensions_override: list[int] = None
    ):
        """Checks if the given point is within the object's dimensions."""
        box: list[int] = (
            dimensions_override
            if dimensions_override is not None
            else self.hitbox
            if hasattr(self, "hitbox")
            else self.dimensions
        )
        return (
            box[0] < mouse_pos[0] < box[0] + box[2]
            and box[1] < mouse_pos[1] < box[1] + box[3]
        )


class ShopItem(Clickable):
    """Abstract class for shop item that is clickable."""

    def __init__(self, pos: tuple[int, int], name: str | int, cost: int):
        self.x_pos, self.y_pos = pos
        self.name = name
        self.cost = cost

    @property
    def affordable(self):
        """Whether or not the player's balance is sufficient to buy this item."""
        return variables.money_count >= self.cost
