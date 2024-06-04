import tkinter as tk
from tkinter import filedialog, messagebox
class GameEngine:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path

        project_window = tk.Toplevel(self.root)
        project_window.title("Project: " + file_path)

        project_frame = tk.Frame(project_window)
        project_frame.pack(fill="both", expand=True)

        export_button = tk.Button(project_frame, text="Экспортировать в C", command=self.export_to_c)
        export_button.pack(pady=10)

        editor_frame = tk.Frame(project_frame)
        editor_frame.pack(fill="both", expand=True)

        code_text = tk.Text(editor_frame, width=40, height=20)
        code_text.pack(fill="both", expand=True)

        with open(file_path, "r") as file:
            code_text.insert(tk.END, file.read())

    def export_to_c(self):
        # Экспортировать проект в C
        project_name = self.file_path.split(".")[0]
        c_file_path = f"{project_name}.c"

        with open(c_file_path, "w") as file:
            code_text = self.code_text.get("1.0", tk.END)
            file.write(code_text)

        print(f"Проект экспортирован в файл: {c_file_path}")