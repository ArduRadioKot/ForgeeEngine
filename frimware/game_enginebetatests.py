import tkinter as tk
from tkinter import ttk
import ast

class GameConstructor:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Constructor")
        self.master.geometry("800x600")

        self.blocks_frame = tk.Frame(self.master, bg="gray")
        self.blocks_frame.pack(side="left", fill="y")

        self.blocks_list = tk.Listbox(self.blocks_frame, width=20, height=10)
        self.blocks_list.pack(fill="both", expand=True)

        self.blocks_list.insert(tk.END, "Move Forward")
        self.blocks_list.insert(tk.END, "Turn Left")
        self.blocks_list.insert(tk.END, "Turn Right")
        self.blocks_list.insert(tk.END, "Jump")
        self.blocks_list.insert(tk.END, "If-Then")
        self.blocks_list.insert(tk.END, "Repeat")

        self.code_frame = tk.Frame(self.master, bg="white")
        self.code_frame.pack(side="right", fill="both", expand=True)

        self.code_text = tk.Text(self.code_frame, width=40, height=20)
        self.code_text.pack(fill="both", expand=True)

        self.export_button = tk.Button(self.master, text="Export to C", command=self.export_to_c)
        self.export_button.pack(side="bottom", fill="x")

    def add_block(self, event):
        selected_block = self.blocks_list.get(self.blocks_list.curselection())
        self.code_text.insert(tk.END, f"{selected_block}\n")

    def export_to_c(self):
        code = self.code_text.get("1.0", "end-1c")
        ast_tree = ast.parse(code)
        c_code = self.generate_c_code(ast_tree)
        print(c_code)

    def generate_c_code(self, ast_tree):
        # Здесь должна быть реализована логика генерации кода на C
        # из абстрактного синтаксического дерева (AST)
        # для микроконтроллера
        pass

root = tk.Tk()
app = GameConstructor(root)
root.mainloop()