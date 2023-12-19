class Clickable:
    def is_hovered(self, mouse_pos: tuple[int, int]):
        return (
            self.dimensions[0] < mouse_pos[0] < self.dimensions[0] + self.dimensions[2]
            and self.dimensions[1]
            < mouse_pos[1]
            < self.dimensions[1] + self.dimensions[3]
        )
