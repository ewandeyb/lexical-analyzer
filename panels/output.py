import tkinter as tk


class OutputPanel(tk.Frame):
    bg = "#7D5AA3"

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(master=parent, bg=self.bg, *args, **kwargs)
