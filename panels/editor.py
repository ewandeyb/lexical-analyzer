import tkinter as tk


class EditorPanel(tk.Frame):
    bg = "#B7D06B"

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(master=parent, bg=self.bg, *args, **kwargs)

        self.init_editor()

    def init_editor(self):
        self.editor = tk.Text(self)
        self.editor.pack(expand=True, fill="both")
