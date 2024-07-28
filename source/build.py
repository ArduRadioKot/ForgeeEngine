import tkinter
import tkinter.messagebox
import customtkinter
import customtkinter as ctk
from tkinter import simpledialog, filedialog, messagebox
from customtkinter import CTk, CTkLabel, CTkButton,  CTkToplevel
import tkinter as tk
from PIL import Image, ImageTk
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green") 

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("ForgeeEngine")
        self.root.geometry("800x600")

        self.menu_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.label = ctk.CTkLabel(self.menu_frame, text="ForgeeEngine", font=("Arial", 24))
        self.label.pack(pady=20)

        self.open_project_button = ctk.CTkButton(self.menu_frame, text="Открыть проект", command=self.open_project)
        self.open_project_button.pack(pady=10)

        self.create_project_button = ctk.CTkButton(self.menu_frame, text="Создать проект", command=self.create_project)
        self.create_project_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self.menu_frame, text="Выйти", command=self.quit)
        self.quit_button.pack(pady=10)

        self.recent_projects_label = ctk.CTkLabel(self.menu_frame, text="Недавно созданные проекты:")
        self.recent_projects_label.pack(pady=10)

        self.recent_projects_combobox = ctk.CTkComboBox(self.menu_frame, values=[], command=self.open_recent_project)
        self.recent_projects_combobox.pack(pady=10)
        self.recent_projects_list = []

    def quit(self):
        self.root.destroy()

    def open_project(self):
        file_path = filedialog.askopenfilename(title="Выберите проект", filetypes=[("Game Engine Projects", "*.fge")])
        if file_path:
            game_engine_window = ctk.CTkToplevel(self.root)
            game_engine = GameEngine(game_engine_window, file_path)

    def create_project(self):
        create_window = ctk.CTkToplevel(self.root)
        create_window.title("Создать проект")

        create_frame = ctk.CTkFrame(create_window, corner_radius=10)
        create_frame.pack(fill="both", expand=True, padx=10, pady=10)

        project_name_label = ctk.CTkLabel(create_frame, text="Название проекта:")
        project_name_label.pack(pady=10)

        project_name_entry = ctk.CTkEntry(create_frame, width=200)
        project_name_entry.pack(pady=10)

        create_button = ctk.CTkButton(create_frame, text="Создать проект", command=lambda: self.create_project_file(project_name_entry.get()))
        create_button.pack(pady=10)

    def create_project_file(self, project_name):

        self.recent_projects_combobox.configure(values=self.recent_projects_list + [project_name])

        game_engine_window = ctk.CTkToplevel(self.root)
        game_engine = GameEngine(game_engine_window)  # Create GameEngine window without file path

    def open_recent_project(self, project_name):
        game_engine_window = ctk.CTkToplevel(self.root)
        game_engine = GameEngine(game_engine_window, project_name)

    def settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Настройки")

        settings_frame = ctk.CTkFrame(settings_window, corner_radius=10)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        setting_label = ctk.CTkLabel(settings_frame, text="Настройка:")
        setting_label.pack(pady=10)

        setting_entry = ctk.CTkEntry(settings_frame, width=200)
        setting_entry.pack(pady=10)

        save_button = ctk.CTkButton(settings_frame, text="Сохранить настройки", command=lambda: self.save_settings(setting_entry.get()))
        save_button.pack(pady=10)

    def save_settings(self, setting):
        print(f"Настройка сохранена: {setting}")


class GameEngine:
    def __init__(self, master: ctk.CTk):
        
        self.master = master
        self.master.title("blockcoding")
        self.master.geometry("1367x768")

        self.canvas = ctk.CTkCanvas(self.master, width=1200, height=1000000)
        self.canvas.pack(side="left")
        self.scroll_region = (0, 0, 1000, 1000)
        self.canvas.config(scrollregion=self.scroll_region)
        
        self.elements = []

        self.trash_zone = ctk.CTkFrame(self.master, bg_color="red", width=100, height=200)
        self.trash_zone.pack(side="right", fill="both", expand=True)
        
        self.button_frame = ctk.CTkFrame(self.master)
        self.button_frame.pack()

        self.v_scroll = ctk.CTkScrollbar(self.master, orientation="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.v_scroll.set)
        
        
        self.blocks = {
            'ledON': {'code': 'digitalWrite(LED_PIN, HIGH);', 'params': [], 'index': 1},
            'ledOFF': {'code': 'digitalWrite(LED_PIN, LOW);', 'params': [], 'index': 2},
            'loop': {'code': 'void endless_loop()', 'params': [], 'index': 3},
            'if': {'code': 'if (%s) {\n    %s\n}', 'params': ['condition', 'body'], 'index': 4},
            'buttonON': {'code': 'if (digitalRead(buttonPin) == HIGH)', 'params': [], 'index': 5},
            'buttonOFF': {'code': 'if (digitalRead(buttonPin) == LOW)', 'params': [], 'index': 6},
            'else': {'code': 'else', 'params': [], 'index': 7},
            'do': {'code': '{', 'params': [], 'index': 8},
            'end': {'code': '}', 'params': [], 'index': 9},
            'delay': {'code': 'sleep(1000);', 'params': [], 'index': 10},
        }
        
        self.create_buttons()

        self.export_button = ctk.CTkButton(self.button_frame, text="Save", command=self.save_logical_elements)
        self.export_button.pack(fill="x")

        self.export_button = ctk.CTkButton(self.button_frame, text="Open", command=self.open_logical_elements)
        self.export_button.pack(fill="x")

        self.export_button = ctk.CTkButton(self.button_frame, text="Custom element", command=self.create_custom_element)
        self.export_button.pack(fill="x")

        self.export_button = ctk.CTkButton(self.button_frame, text="Export to C", command=self.export_to_c)
        self.export_button.pack(fill="x")

    def create_buttons(self):
        for block_name, block_info in self.blocks.items():
            button = ctk.CTkButton(self.button_frame, text=block_name, command=lambda block_name=block_name: self.create_block(block_name))
            button.pack(fill="x")

    def create_block(self, block_name):
        block_info = self.blocks[block_name]
        block = ctk.CTkLabel(self.master, text=f"{block_name} ({block_info['index']})", bg_color="white", text_color="black")
        block.draggable = True
        block.params = block_info['params']
        block.bind("<ButtonPress-1>", self.start_drag)
        block.bind("<ButtonRelease-1>", self.stop_drag)
        block.bind("<B1-Motion>", self.drag)
        block.bind("<Button-3>", self.show_context_menu)
        self.elements.append(block)
        self.canvas.create_window(10, 10, window=block, tags=f"block_{block_name}")
        block.canvas_id = self.canvas.find_withtag(f"block_{block_name}")[0]



    def start_drag(self, event: tk.Event):
        element = event.widget
        element.x0 = event.x
        element.y0 = event.y

    def stop_drag(self, event: tk.Event):
        element = event.widget
        if self.is_in_trash_zone(element):
            self.delete_element(element)

    def drag(self, event: tk.Event):
        element = event.widget
        dx = event.x - element.x0
        dy = event.y - element.y0
        self.canvas.move(element.canvas_id, dx, dy)
        element.x0 = event.x
        element.y0 = event.y

    def is_in_trash_zone(self, element: ctk.CTkLabel):
        x, y = element.winfo_x(), element.winfo_y()
        return (x > self.trash_zone.winfo_x() and
                x < self.trash_zone.winfo_x() + self.trash_zone.winfo_width() and
                y > self.trash_zone.winfo_y() and
                y < self.trash_zone.winfo_y() + self.trash_zone.winfo_height())

    def delete_element(self, element: ctk.CTkLabel):
        element.destroy()
        self.elements.remove(element)

    def export_to_c(self):
        code = ""
        for element in self.elements:
            if isinstance(element, ctk.CTkText):  # Check if element is a Text widget
                block_text = element.get("1.0", "end-1c")  # Get entire text of the block
                code += block_text + "\n"
            else:
                block_name = element.cget("text").split(" (")[0]
                if block_name in self.blocks:
                    block_info = self.blocks[block_name]
                    params = self.get_block_params(block_name)
                    code += block_info["code"] % tuple(params) + "\n"
                else:
                    code += element.cget("text") + "\n"
        file_path = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[('C files', '*.c')])
        if file_path:
            with open(file_path, "w") as f:
                f.write(code)

    def get_block_params(self, block_name):
        block_info = self.blocks[block_name]
        if block_info['params']:
            return [simpledialog.askstring("Parameter", f"Enter value for {param}") for param in block_info["params"]]
        return []

    def save_logical_elements(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".fcb", filetypes=[('ForgeeCodeIDE_block', '*.fcb')])
        if file_path:
            with open(file_path, "w") as f:
                for element in self.elements:
                    x, y = element.winfo_rootx(), element.winfo_rooty()
                    f.write(f"{element.cget('text')} {x} {y}\n")
            print("Logical scheme saved to logical_scheme.lgs")

    def open_logical_elements(self):
        file_path = filedialog.askopenfilename(filetypes=[("ForgeeCodeIDE_block", "*.fcb")])
        if file_path:
            self.elements = []
            with open(file_path, "r") as f:
                for line in f:
                    text, x, y = line.strip().split()
                    x, y = int(x), int(y)
                    block_name = text.split(" (")[0]
                    element = ctk.CTkLabel(self.master, text=text, bg_color="white", text_color="black", width=5, height=2)
                    element.place(x=x, y=y)
                    element.draggable = True
                    element.bind("<ButtonPress-1>", self.start_drag)
                    element.bind("<ButtonRelease-1>", self.stop_drag)
                    element.bind("<B1-Motion>", self.drag)
                    element.bind("<Button-3>", self.show_context_menu)
                    self.elements.append(element)

    def create_custom_element(self):
        custom_element_window = ctk.CTkToplevel(self.master)
        custom_element_window.title("Create Custom block")

        text_editor = ctk.CTkTextbox(custom_element_window, width=400, height=100)

        text_editor.pack(fill="both", expand=True)

        create_button = ctk.CTkButton(custom_element_window, text="Create", command=lambda: self.add_custom_element(text_editor.get("1.0", "end-1c")))
        create_button.pack()

    def add_custom_element(self, element_text: str):
        custom_element = ctk.CTkTextbox(self.master, width=200, height=50)
        custom_element.insert("1.0", element_text)
        custom_element.draggable = True
        custom_element.bind("<ButtonPress-1>", self.start_drag)
        custom_element.bind("<ButtonRelease-1>", self.stop_drag)
        custom_element.bind("<B1-Motion>", self.drag)
        custom_element.bind("<Button-3>", self.show_context_menu)
        self.elements.append(custom_element)
        canvas_id = self.canvas.create_window(10, 10, window=custom_element, tags="custom_element")
        custom_element.canvas_id = canvas_id

    def show_context_menu(self, event: tk.Event):
        context_menu = ctk.CTkMenu(self.master, tearoff=0)
        context_menu.add_command(label="Delete", command=lambda: self.delete_element(event.widget))
        context_menu.add_command(label="Edit Parameters", command=lambda: self.edit_parameters(event.widget))
        context_menu.post(event.x_root, event.y_root)

    def edit_parameters(self, element):
        block_name = element.cget("text").split(" (")[0]
        block_info = self.blocks[block_name]
        if block_info["params"]:
            params = [simpledialog.askstring("Parameter", f"Enter value for {param}") for param in block_info["params"]]
            block_info["code"] = block_info["code"] % tuple(params)
        else:
            messagebox.showinfo("No Parameters", "This block has no parameters to edit.")


root = ctk.CTk()
main_app = MainMenu(root) 
root.mainloop()