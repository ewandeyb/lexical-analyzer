import tkinter as tk


class EditorPanel(tk.Frame):
    bg = "#B7D06B"

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(master=parent, bg=self.bg, *args, **kwargs)

        self.grid(row=0, column=0, sticky="nsew")
