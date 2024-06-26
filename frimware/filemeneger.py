import os
import tkinter as tk
from tkinter import filedialog, messagebox

class FileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("800x600")

        # Создаем панель инструментов
        self.toolbar = tk.Frame(self.root, bg="gray")
        self.toolbar.pack(fill="x")

        # Кнопка "Открыть файл"
        self.open_button = tk.Button(self.toolbar, text="Открыть файл", command=self.open_file)
        self.open_button.pack(side="left", padx=5, pady=5)

        # Кнопка "Создать файл"
        self.create_button = tk.Button(self.toolbar, text="Создать файл", command=self.create_file)
        self.create_button.pack(side="left", padx=5, pady=5)

        # Кнопка "Удалить файл"
        self.delete_button = tk.Button(self.toolbar, text="Удалить файл", command=self.delete_file)
        self.delete_button.pack(side="left", padx=5, pady=5)

        # Создаем список файлов
        self.file_list = tk.Listbox(self.root, width=80)
        self.file_list.pack(fill="both", expand=True)

        # Создаем поле ввода для пути к файлу
        self.path_entry = tk.Entry(self.root, width=80)
        self.path_entry.pack(fill="x", padx=5, pady=5)

        # Создаем кнопку "Перейти"
        self.go_button = tk.Button(self.root, text="Перейти", command=self.go_to_path)
        self.go_button.pack(fill="x", padx=5, pady=5)

        # Инициализируем список файлов
        self.update_file_list()

    def open_file(self):
        # Открываем файл с помощью диалога
        file_path = filedialog.askopenfilename()
        if file_path:
            os.startfile(file_path)

    def create_file(self):
        # Создаем файл с помощью диалога
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as f:
                f.write("")
            self.update_file_list()

    def delete_file(self):
        # Удаляем файл
        selected_file = self.file_list.get(self.file_list.curselection())
        if selected_file:
            os.remove(selected_file)
            self.update_file_list()

    def go_to_path(self):
        # Переходим к указанному пути
        path = self.path_entry.get()
        if os.path.exists(path):
            self.update_file_list(path)
        else:
            messagebox.showerror("Ошибка", "Путь не существует")

    def update_file_list(self, path="."):
        # Обновляем список файлов
        self.file_list.delete(0, tk.END)
        for file in os.listdir(path):
            self.file_list.insert(tk.END, os.path.join(path, file))

root = tk.Tk()
file_manager = FileManager(root)
root.mainloop()