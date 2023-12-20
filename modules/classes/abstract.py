"""Definitions of abstract classes that other classes will inherit from."""


class Clickable:
    """Abstract class for objects which will be hovered over or clicked by the user's mouse."""

    dimensions: list[int]

    def is_hovered(self, mouse_pos: tuple[int, int]):
        """Checks if the given point is within the object's dimensions."""
        box: list[int] = self.hitbox if hasattr(self, "hitbox") else self.dimensions
        return (
            box[0] < mouse_pos[0] < box[0] + box[2]
            and box[1] < mouse_pos[1] < box[1] + box[3]
        )
