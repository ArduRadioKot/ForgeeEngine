import tkinter as tk
from tkinter import ttk

class GameBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Builder")
        self.root.geometry("800x600")

        # Создаем меню
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_project)
        self.file_menu.add_command(label="Open", command=self.open_project)
        self.file_menu.add_command(label="Save", command=self.save_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        # Создаем панель инструментов
        self.toolbar = tk.Frame(self.root, bg="gray")
        self.toolbar.pack(fill="x")

        self.new_button = tk.Button(self.toolbar, text="New", command=self.new_project)
        self.new_button.pack(side="left")

        self.open_button = tk.Button(self.toolbar, text="Open", command=self.open_project)
        self.open_button.pack(side="left")

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_project)
        self.save_button.pack(side="left")

        # Создаем область для создания игры
        self.game_area = tk.Frame(self.root, bg="white")
        self.game_area.pack(fill="both", expand=True)

        # Создаем список объектов
        self.object_list = tk.Listbox(self.game_area, width=20)
        self.object_list.pack(side="left", fill="y")

        # Создаем область для свойств объектов
        self.properties_area = tk.Frame(self.game_area, bg="gray")
        self.properties_area.pack(side="right", fill="y")

        # Создаем кнопки для добавления объектов
        self.add_button = tk.Button(self.game_area, text="Add Object", command=self.add_object)
        self.add_button.pack(side="bottom")

    def new_project(self):
        print("New project")

    def open_project(self):
        print("Open project")

    def save_project(self):
        print("Save project")

    def add_object(self):
        object_name = tk.simpledialog.askstring("Add Object", "Enter object name")
        if object_name:
            self.object_list.insert(tk.END, object_name)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game_builder = GameBuilder(root)
    game_builder.run()