import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText

class GameEngine:
    def __init__(self, root, master: tk.Tk):
        self.root = root
        self.master = master
        self.master.title("blockcoding")
        self.master.geometry("1367x768")

        self.canvas = tk.Canvas(self.master, width=1200, height=1000000, bg="gray")
        self.canvas.pack(side="left")
        self.scroll_region = (0, 0, 1000, 1000)
        self.canvas.config(scrollregion=self.scroll_region)
        
        self.elements = []

        self.trash_zone = tk.Frame(self.master, bg="red", width=100, height=200)
        self.trash_zone.pack(side="right", fill="both", expand=True)
        
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        self.v_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
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
        self.toolbar = tk.Frame(self.root, bg="gray")
        self.toolbar.pack(fill="x")
        self.export_button = tk.Button(self.toolbar, text="Save", command=self.save_logical_elements)
        self.export_button.pack(side="left", padx=5, pady=5)

        self.export_button = tk.Button(self.toolbar, text="Open", command=self.open_logical_elements)
        self.export_button.pack(side="left", padx=5, pady=5)

        self.export_button = tk.Button(self.toolbar, text="Custom element", command=self.create_custom_element)
        self.export_button.pack(side="left", padx=5, pady=5)

        self.import_button = tk.Button(self.toolbar, text="Import from C", command=self.import_blocks_from_c_file)
        self.import_button.pack(side="left", padx=5, pady=5)

        self.export_button = tk.Button(self.toolbar, text="Export to C", command=self.export_to_c)
        self.export_button.pack(side="left", padx=5, pady=5)

    def create_buttons(self):
        for block_name, block_info in self.blocks.items():
            button = tk.Button(self.button_frame, text=block_name, command=lambda block_name=block_name: self.create_block(block_name))
            button.pack(fill="x")

    def create_block(self, block_name):
        block_info = self.blocks[block_name]
        block = tk.Label(self.master, text=f"{block_name} ({block_info['index']})", bg="white", fg="black")
        block.draggable = True
        block.params = block_info['params']
        block.bind("<ButtonPress-1>", self.start_drag)
        block.bind("<ButtonRelease-1>", self.stop_drag)
        block.bind("<B1-Motion>", self.drag)
        block.bind("<Button-3>", self.show_context_menu)
        self.elements.append(block)
        self.canvas.create_window(10, 10, window=block)

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
        element.place(x=element.winfo_x() + dx, y=element.winfo_y() + dy)
        element.x0 = event.x
        element.y0 = event.y

    def is_in_trash_zone(self, element: tk.Label):
        x, y = element.winfo_x(), element.winfo_y()
        return (x > self.trash_zone.winfo_x() and
                x < self.trash_zone.winfo_x() + self.trash_zone.winfo_width() and
                y > self.trash_zone.winfo_y() and
                y < self.trash_zone.winfo_y() + self.trash_zone.winfo_height())

    def delete_element(self, element: tk.Label):
        element.destroy()
        self.elements.remove(element)

    def export_to_c(self):
        code = ""
        for element in self.elements:
            if isinstance(element, tk.Text):  # Check if element is a Text widget
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
                    element = tk.Label(self.master, text=text, bg="white", fg="black", width=5, height=2)
                    element.place(x=x, y=y)
                    element.draggable = True
                    element.bind("<ButtonPress-1>", self.start_drag)
                    element.bind("<ButtonRelease-1>", self.stop_drag)
                    element.bind("<B1-Motion>", self.drag)
                    element.bind("<Button-3>", self.show_context_menu)
                    self.elements.append(element)

    def create_custom_element(self):
        custom_element_window = tk.Toplevel(self.master)
        custom_element_window.title("Create Custom Logical Element")

        text_editor = ScrolledText(custom_element_window, width=40, height=10)
        text_editor.pack(fill="both", expand=True)

        create_button = tk.Button(custom_element_window, text="Create", command=lambda: self.add_custom_element(text_editor.get("1.0", "end-1c")))
        create_button.pack()

    def add_custom_element(self, element_text: str):
        custom_element = tk.Text(self.master, width=20, height=5)
        custom_element.insert("1.0", element_text)
        custom_element.draggable = True
        custom_element.bind("<ButtonPress-1>", self.start_drag)
        custom_element.bind("<ButtonRelease-1>", self.stop_drag)
        custom_element.bind("<B1-Motion>", self.drag)
        custom_element.bind("<Button-3>", self.show_context_menu)
        self.elements.append(custom_element)
        self.canvas.create_window(10, 10, window=custom_element)

    def show_context_menu(self, event: tk.Event):
        context_menu = tk.Menu(self.master, tearoff=0)
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

    def import_blocks_from_c_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C files", "*.c")])
        if file_path:
            with open(file_path, "r") as f:
                c_code = f.read()
            self.parse_c_code(c_code)

    def parse_c_code(self, c_code: str):
    # Very basic parsing, you may want to improve this
        blocks = []
        for line in c_code.splitlines():
            if line.startswith("void ") and "(" in line and ")" in line:
                block_name = line.split("(")[0].strip().replace("void ", "")
                block_code = line
                blocks.append({"name": block_name, "code": block_code, "params": self.extract_params(block_code)})
        for block in blocks:
            self.add_custom_block(block)

    def extract_params(self, block_code: str):
    # Very basic parameter extraction, you may want to improve this
        params = []
        start_idx = block_code.find("(")
        end_idx = block_code.find(")")
        if start_idx != -1 and end_idx != -1:
            param_str = block_code[start_idx + 1:end_idx]
            params = [param.strip() for param in param_str.split(",")]
        return params

    def add_custom_block(self, block_info: dict):
        block_name = block_info["name"]
        block_code = block_info["code"]
        block_params = block_info["params"]
        self.blocks[block_name] = {"code": block_code, "params": block_params, "index": len(self.blocks) + 1}
        button = tk.Button(self.button_frame, text=block_name, command=lambda block_name=block_name: self.create_block(block_name))
        button.pack(fill="x")
        self.create_block(block_name)  # Create the block immediately

root = tk.Tk()
main_app = GameEngine(root=root) 
root.mainloop()