"""Fake module to import when the user is on a non-Windows operating system."""


def set_cursor_pos(joystick) -> None:
    """No-op."""
