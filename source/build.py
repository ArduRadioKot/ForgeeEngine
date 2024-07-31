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
        self.root = master
        self.master.title("blockcoding")
        self.master.geometry("1367x768")

        self.toolbar = ctk.CTkFrame(self.master, width=50, height=768)
        self.toolbar.pack(side="left", fill="y")

        self.label = ctk.CTkLabel(self.toolbar, text="ForgeeEngine", font=("Arial", 15))
        self.label.pack(pady=10)

        self.paint_button = ctk.CTkButton(self.toolbar, text="Paint", command=self.paint)
        self.paint_button.pack(fill="x", pady=10)

        self.ide_button = ctk.CTkButton(self.toolbar, text="IDE")
        self.ide_button.pack(fill="x", pady=10)

        self.settings_button = ctk.CTkButton(self.toolbar, text="Settings")
        self.settings_button.pack(fill="x", pady=10)

        self.settings_button = ctk.CTkButton(self.toolbar, text="Quit")
        self.settings_button.pack(fill="x", pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.toolbar, text="Appearance Mode:")
        self.appearance_mode_label.pack(fill="x", pady=140)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.toolbar, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(fill="x", pady=10)
        self.scaling_label = ctk.CTkLabel(self.toolbar, text="UI Scaling:")
        self.scaling_label.pack(fill="x", pady=10)
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.toolbar, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.pack(fill="x", pady=10)
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
        self.export_button.pack(fill="x", pady =10)

        self.export_button = ctk.CTkButton(self.button_frame, text="Open", command=self.open_logical_elements)
        self.export_button.pack(fill="x",pady =10)

        self.export_button = ctk.CTkButton(self.button_frame, text="Custom element", command=self.create_custom_element)
        self.export_button.pack(fill="x", pady =10)

        self.export_button = ctk.CTkButton(self.button_frame, text="Export to C", command=self.export_to_c)
        self.export_button.pack(fill="x", pady =10)

    def create_buttons(self):
        for block_name, block_info in self.blocks.items():
            button = ctk.CTkButton(self.button_frame, text=block_name, command=lambda block_name=block_name: self.create_block(block_name))
            button.pack(fill="x", pady =10 )

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

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    def paint(self):
        paint_window = ctk.CTkToplevel(self.root)
        paint_engine = PaintEngine(paint_window)  # Pass the master parameter
        paint_engine.run()  # Call the run method to start the event loop # Call the run method to start the event loop

class PaintEngine:
    def __init__(self, master):
        self.root = ctk.CTk()
        self.master = master
        self.root.title("Черно-белый экран")
        self.root.geometry("800x640")

        self.canvas = ctk.CTkCanvas(self.root, width=512, height=256, background="white")        
        self.canvas.pack(pady=20, padx=10)

        self.pixel_size = 4  # размер пикселя в пикселях
        for i in range(64):  # 16 строк
            for j in range(128):  # 32 столбца
                x1 = j * self.pixel_size
                y1 = i * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        self.brush_size = 1
        self.eraser_size = 1

        self.brush_slider = ctk.CTkSlider(self.root, from_=1, to=10, width=200, command=self.update_brush_size)
        self.brush_slider.pack(pady=10)
        self.brush_label = ctk.CTkLabel(self.root, text="Brush size: 1")
        self.brush_label.pack()

        self.eraser_slider = ctk.CTkSlider(self.root, from_=1, to=10, width=200, command=self.update_eraser_size)
        self.eraser_slider.pack(pady=10)
        self.eraser_label = ctk.CTkLabel(self.root, text="Eraser size: 1")
        self.eraser_label.pack()

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<B3-Motion>", self.erase)

        self.save_button = ctk.CTkButton(self.root, text="Save bitmap", command=self.save_bitmap_h)
        self.save_button.pack(pady=20)

        self.open_button = ctk.CTkButton(self.root, text="Open image", command=self.open_image)
        self.open_button.pack()

        self.save_button = ctk.CTkButton(self.root, text="Quit", command=self.quit)
        self.save_button.pack(pady=20)

        self.image = None
    
    def quit(self):
        self.root.destroy()

    def paint_pixel(self, x, y, color, brush_size):
        for i in range(-brush_size, brush_size+1):
            for j in range(-brush_size, brush_size+1):
                x1 = (x + i) * self.pixel_size
                y1 = (y + j) * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def draw(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        self.paint_pixel(x, y, "black", self.brush_size)

    def erase(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        self.paint_pixel(x, y, "white", self.eraser_size)

    def save_bitmap_h(self):
        bitmap = []
        for i in range(64):  # 64 строки для 128x64 пикселей
            byte = 0
            for j in range(128):  # 128 пикселей в строке
                x = j
                y = i
                item_id = self.canvas.find_closest(x*self.pixel_size, y*self.pixel_size)
                pixel_color = self.canvas.itemcget(item_id, "fill")
                if pixel_color == "black":
                    byte |= 1 << (7 - (j % 8))  # битовая операция для формирования байта
                if j % 8 == 7:  # каждые 8 пикселей - новый байт
                    bitmap.append("0x{:02x}".format(byte))  # Convert integer to hex string
                    byte = 0
        with open("bitmap.h", "w") as f:
            f.write("const uint8_t bitmap[] = {\n")
            for i in range(0, len(bitmap), 16):
                f.write(", ".join(bitmap[i:i+16]) + ",\n")
            f.write("};\n")

    def update_brush_size(self, value):
        self.brush_size = int(value)
        self.brush_label.configure(text=f"Brush size: {self.brush_size}")

    def update_eraser_size(self, value):
        self.eraser_size = int(value)
        self.eraser_label.configure(text=f"Eraser size: {self.eraser_size}")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ".png .jpg .bmp")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((128, 64))
            self.image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")  # Очистить канву перед отображением нового изображения
            self.canvas.create_image(0, 0, image=self.image, anchor="nw")
            self.canvas.image = self.image  # Сохранить ссылку на изображение

    def run(self):
        self.root.mainloop()
root = ctk.CTk()
main_app = MainMenu(root) 
root.mainloop()