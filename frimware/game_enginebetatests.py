import tkinter as tk
from tkinter import filedialog
import json

class GameCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Creator")
        self.root.geometry("800x600")

        self.scene = tk.Canvas(self.root, width=400, height=400)
        self.scene.pack(side=tk.LEFT)

        self.object_list = tk.Listbox(self.root, width=40)
        self.object_list.pack(side=tk.LEFT)

        self.property_frame = tk.Frame(self.root)
        self.property_frame.pack(side=tk.LEFT)

        self.create_menu()

        self.objects = []
        self.current_object = None

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Open Game", command=self.open_game)
        filemenu.add_command(label="Save Game", command=self.save_game)
        filemenu.add_command(label="Export to C", command=self.export_to_c)
        menubar.add_cascade(label="File", menu=filemenu)

        objectmenu = tk.Menu(menubar, tearoff=0)
        objectmenu.add_command(label="Create Object", command=self.create_object)
        objectmenu.add_command(label="Delete Object", command=self.delete_object)
        menubar.add_cascade(label="Object", menu=objectmenu)

    def new_game(self):
        self.objects = []
        self.object_list.delete(0, tk.END)
        self.scene.delete(tk.ALL)

    def open_game(self):
        filename = filedialog.askopenfilename(title="Open Game", filetypes=[("Game Files", "*.game")])
        if filename:
            with open(filename, "r") as f:
                self.objects = json.load(f)
            self.object_list.delete(0, tk.END)
            for obj in self.objects:
                self.object_list.insert(tk.END, obj["name"])
            self.scene.delete(tk.ALL)
            for obj in self.objects:
                self.scene.create_oval(obj["x"], obj["y"], obj["x"] + 20, obj["y"] + 20, fill=obj["color"])

    def save_game(self):
        filename = filedialog.asksaveasfilename(title="Save Game", filetypes=[("Game Files", "*.game")])
        if filename:
            with open(filename, "w") as f:
                json.dump(self.objects, f)

    def export_to_c(self):
        filename = filedialog.asksaveasfilename(title="Export to C", filetypes=[("C Files", "*.c")])
        if filename:
            with open(filename, "w") as f:
                f.write("#include <ch32v003.h>\n")
                f.write("void setup() {\n")
                for obj in self.objects:
                    f.write(f"  draw_rect({obj['x']}, {obj['y']}, {obj['x'] + 20}, {obj['y'] + 20}, {obj['color']});\n")
                f.write("}\n")

    def create_object(self):
        obj_name = tk.simpledialog.askstring("Create Object", "Enter object name")
        if obj_name:
            obj = {"name": obj_name, "x": 100, "y": 100, "color": "red"}
            self.objects.append(obj)
            self.object_list.insert(tk.END, obj_name)
            self.scene.create_oval(obj["x"], obj["y"], obj["x"] + 20, obj["y"] + 20, fill=obj["color"])

    def delete_object(self):
        selected_index = self.object_list.curselection()
        if selected_index:
            self.object_list.delete(selected_index)
            del self.objects[selected_index[0]]
            self.scene.delete(tk.ALL)
            for obj in self.objects:
                self.scene.create_oval(obj["x"], obj["y"], obj["x"] + 20, obj["y"] + 20, fill=obj["color"])

root = tk.Tk()
game_creator = GameCreator(root)
root.mainloop()