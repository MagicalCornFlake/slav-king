"""Module containing auxiliary GUI elements such as popup modals."""

import tkinter
from tkinter import ttk, messagebox

tk_root = tkinter.Tk()
label_text = tkinter.StringVar()
progressbar = ttk.Progressbar(tk_root, length=200, maximum=200)


# Define custom message box called 'abort/retry/ignore' using Tkinter's template
def ask_abort_retry_ignore(
    title: str = None,
    message: str = None,
    _icon: str = messagebox.WARNING,
    _type: str = messagebox.ABORTRETRYIGNORE,
    **options,
) -> str:
    """Create an ABORT/RETRY/IGNORE message box.

    Args:
        title (str, optional): the dialog box title. Defaults to None.
        message (str, optional): the dialog box message. Defaults to None.
        _icon (str, optional): the dialog box icon. Defaults to tkinter.messagebox.WARNING.
        _type (str, optional): the dialog box type. Defaults to tkinter.messagebox.ABORTRETRYIGNORE.

    Returns:
        str: the user response ("yes"/"no" etc.).
    """
    if _icon:
        options.setdefault("icon", _icon)
    if _type:
        options.setdefault("type", _type)
    if title:
        options["title"] = title
    if message:
        options["message"] = message
    message_box = messagebox.Message(tk_root, **options)
    res = message_box.show()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        return "yes" if res else "no"
    # In others we get a Tcl_Obj.
    return str(res)


def show_popup(*args, popup_type="info"):
    """Wrapper for `tkinter.messagebox.show*`"""
    hide_root()
    match popup_type:
        case "info":
            messagebox.showinfo(*args)
        case "warning":
            messagebox.showwarning(*args)
        case "error":
            messagebox.showerror(*args)
        case _:
            raise RuntimeError(f"Invalid popup type '{popup_type}'")


def create_progressbar():
    """Creates a progress bar."""
    tk_root.geometry("300x100")
    tk_root.title("Slav King Updater")
    label = tkinter.Label(tk_root, textvariable=label_text, wraplength=280)
    label.place(x=10, y=10)
    progressbar.place(x=50, y=60)
    return progressbar


def update_label(value: str):
    """Sets the label of the progress bar."""
    label_text.set(value)
    tk_root.update()


def increment_progressbar(progress: float = 25.0):
    """Updates the displayed progress in the progress bar."""
    progressbar.step(progress)
    tk_root.update()


def hide_root():
    """Hides the root window."""
    tk_root.update()
    tk_root.wm_withdraw()
