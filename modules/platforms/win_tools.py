"""Module containing Windows-specific functionality."""

from ctypes import windll, Structure, c_long, byref

from pygame.joystick import Joystick


class Point(Structure):
    """Object representing a pixel on the screen."""

    _fields_ = [("x", c_long), ("y", c_long)]

    @property
    def list(self):
        """Point representation as a pair of coordinates."""
        return [self.x, self.y]

    def __repr__(self):
        return f"{self.x}, {self.y}"


def get_cursor_pos() -> Point:
    """Gets the mouse cursor position on the screen using the Windows system tools."""
    mouse_abs_pos = Point()
    windll.user32.GetCursorPos(byref(mouse_abs_pos))
    return mouse_abs_pos


def set_cursor_pos(joystick: Joystick) -> None:
    """Updates the cursor position according to the joystick's axis positions."""
    mouse_abs_pos = get_cursor_pos()
    axis_x = joystick.get_axis(2)
    axis_y = joystick.get_axis(3)
    new_mouse_pos = [mouse_abs_pos.x, mouse_abs_pos.y]
    for axis, axis_val in enumerate([axis_x, axis_y]):
        # Allow for stick drift
        if abs(axis_val) > 0.1:
            new_mouse_pos[axis] += round(20 * axis_val)
    if mouse_abs_pos.list == new_mouse_pos:
        return
    windll.user32.SetCursorPos(*new_mouse_pos)
    # ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
