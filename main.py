import tkinter as tk

def ui(root: tk.Tk) -> None:
    root.title("Lexical Analyzer")
    root.geometry("900x560")

    # Outer frame acts as the blue border
    outer = tk.Frame(root, bg="#2F5F9E", bd=6, relief="flat")
    outer.pack(fill="both", expand=True, padx=8, pady=8)

    # Use grid inside the outer frame
    outer.grid_rowconfigure(1, weight=1)
    outer.grid_columnconfigure(0, weight=1)

    # Main content area
    content = tk.Frame(outer, bg="#50779F")
    content.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
    content.grid_rowconfigure(0, weight=1)
    content.grid_columnconfigure(0, weight=3)
    content.grid_columnconfigure(1, weight=2)

    # Left column which itself will have two stacked panels
    left_col = tk.Frame(content, bg="#50779F")
    left_col.grid(row=0, column=0, sticky="nsew", padx=(6, 3), pady=6)
    left_col.grid_rowconfigure(0, weight=3)
    left_col.grid_rowconfigure(1, weight=1)
    left_col.grid_columnconfigure(0, weight=1)

    # Big green panel (top-left)
    code_editor = tk.Frame(left_col, bg="#B7D06B")
    code_editor.grid(row=0, column=0, sticky="nsew")

    # Orange panel (bottom-left)
    console = tk.Frame(left_col, bg="#F2A65A", height=80)
    console.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

    # Right purple panel
    table_of_vars = tk.Frame(content, bg="#7D5AA3")
    table_of_vars.grid(row=0, column=1, sticky="nsew", padx=(3, 6), pady=6)

def main():
    root = tk.Tk()
    ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()