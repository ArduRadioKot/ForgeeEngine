import tkinter as tk
from tkinter import filedialog, messagebox

class GameMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Maker")
        self.root.geometry("800x600")

        # Меню
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Новый проект", command=self.new_project)
        self.file_menu.add_command(label="Открыть проект", command=self.open_project)
        self.file_menu.add_command(label="Сохранить проект", command=self.save_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.root.quit)
        self.menu.add_cascade(label="Файл", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Добавить объект", command=self.add_object)
        self.edit_menu.add_command(label="Удалить объект", command=self.delete_object)
        self.menu.add_cascade(label="Правка", menu=self.edit_menu)

        # Канва для рисования
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Панель инструментов
        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        self.object_list = tk.Listbox(self.toolbar, width=20)
        self.object_list.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.toolbar, text="Добавить", command=self.add_object)
        self.add_button.pack(fill=tk.X)

        self.delete_button = tk.Button(self.toolbar, text="Удалить", command=self.delete_object)
        self.delete_button.pack(fill=tk.X)

        # Словарь объектов
        self.objects = {}

    def new_project(self):
        self.objects = {}
        self.object_list.delete(0, tk.END)
        self.canvas.delete(tk.ALL)

    def open_project(self):
        filename = filedialog.askopenfilename(title="Открыть проект", filetypes=[("Game Maker files", "*.gm")])
        if filename:
            with open(filename, "r") as f:
                self.objects = eval(f.read())
            self.object_list.delete(0, tk.END)
            for obj in self.objects.values():
                self.object_list.insert(tk.END, obj["name"])
            self.canvas.delete(tk.ALL)
            for obj in self.objects.values():
                self.canvas.create_oval(obj["x"], obj["y"], obj["x"] + 20, obj["y"] + 20, fill=obj["color"])

    def save_project(self):
        filename = filedialog.asksaveasfilename(title="Сохранить проект", filetypes=[("Game Maker files", "*.gm")])
        if filename:
            with open(filename, "w") as f:
                f.write(str(self.objects))

    def add_object(self):
        name = tk.simpledialog.askstring("Добавить объект", "Введите имя объекта")
        if name:
            x = 100
            y = 100
            color = "blue"
            self.objects[name] = {"name": name, "x": x, "y": y, "color": color}
            self.object_list.insert(tk.END, name)
            self.canvas.create_oval(x, y, x + 20, y + 20, fill=color)

    def delete_object(self):
        selected = self.object_list.curselection()
        if selected:
            name = self.object_list.get(selected)
            del self.objects[name]
            self.object_list.delete(selected)
            self.canvas.delete(tk.ALL)
            for obj in self.objects.values():
                self.canvas.create_oval(obj["x"], obj["y"], obj["x"] + 20, obj["y"] + 20, fill=obj["color"])

root = tk.Tk()
game_maker = GameMaker(root)
root.mainloop()