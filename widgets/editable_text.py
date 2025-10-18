import tkinter as tk
from typing import Literal


class EditableText(tk.Text):
    """
    Allows editing of tk.Text using `with` operator.
    """

    def __init__(
        self,
        *args,
        state: Literal["normal", "disabled"] = "disabled",
        **kwargs,
    ) -> None:
        super().__init__(*args, state=state, **kwargs)

    def __enter__(self):
        self._old_state = self.cget("state")
        self.config(state="normal")

        return self

    def __exit__(self, exc_type, exc_val, exc_tbelf):
        self.config(state=self._old_state)

        return False
