# coding: utf-8

"""
This module provide a context manager to switch matplotlib backend
in a notebook environment and a function to switch the backend locally
to inline, which can be useful to stick the figure in the notebook.

Licence MIT
Author: Germain Salvato Vallverdu
"""

import matplotlib.pyplot as plt
from contextlib import contextmanager

_CURRENT_BACKEND = None
__all__ = [
    "mpl_inline_ctx",
    "mpl_use",
]


def mpl_use(backend: str = "widget", verbose: bool = True):
    """Switch matplotlib backend in a notebook environment. The backend can 
    be "widget" or "inline". The function does nothing if the backend 
    is already set to the requested one. All figures are properly closed
    before switching.

    Args:
        backend (str): A valid matplotlib backend, for example "widget" or "inline"
        verbose (bool): whether to print the new backend

    Example:
        mpl_use("widget")  # switch to widget backend
        mpl_use("inline")  # switch to inline backend
    """
    global _CURRENT_BACKEND

    if backend not in ("widget", "inline"):
        raise ValueError("backend must be 'widget' or 'inline'")

    if _CURRENT_BACKEND == backend:
        return

    plt.close("all")

    try:
        ip = get_ipython()
    except NameError:
        raise RuntimeError("You are not in a notebook Jupyter/IPython environment")

    ip.run_line_magic("matplotlib", backend)
    _CURRENT_BACKEND = backend

    if verbose:
        print(f"Matplotlib → {backend}")


import matplotlib.pyplot as plt
from contextlib import contextmanager


@contextmanager
def mpl_inline_ctx():
    """
    Context manager to temporarily switch matplotlib backend to inline.
    That can be useful to save a figure in a notebook without displaying
    it, or to avoid interactive features of the widget backend.

    Only works in Jupyter/IPython.

    Usage:
        with mpl_inline():
            fig, ax = plt.subplots()
            ax.plot(x, y)
            plt.show()
    """
    # Check if we are in IPython
    try:
        ip = get_ipython()
    except NameError:
        raise RuntimeError("You are not in a notebook Jupyter/IPython environment")

    # save current backend
    old_backend = plt.get_backend()

    # close all figures before switch
    plt.close("all")

    # switch to requested backend
    ip.run_line_magic("matplotlib", "inline")

    try:
        yield  # execute the block
    finally:
        # close figures created in the block
        plt.close("all")
        # restore previous backend
        if "inline" in old_backend.lower():
            ip.run_line_magic("matplotlib", "inline")
        elif "widget" in old_backend.lower() or "nbagg" in old_backend.lower():
            ip.run_line_magic("matplotlib", "widget")
        elif "qt" in old_backend.lower():
            ip.run_line_magic("matplotlib", "qt")
        else:
            # fallback to inline if unknown backend
            ip.run_line_magic("matplotlib", "inline")
