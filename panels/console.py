import tkinter as tk


class ConsolePanel(tk.Frame):
    bg = "#F2A65A"

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(master=parent, bg=self.bg, *args, **kwargs)

        self.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
