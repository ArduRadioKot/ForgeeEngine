import customtkinter as ctk
from tkinter import simpledialog, filedialog, messagebox
from customtkinter import CTk, CTkLabel, CTkButton,  CTkToplevel, CTkSwitch, CTkComboBox
import tkinter as tk
import paintforide as p
import TextIde as tide
import json

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue") 

class Block(ctk.CTkFrame):
    def __init__(self, master, block_type, block_info, **kwargs):
        super().__init__(master, **kwargs)
        self.block_type = block_type
        self.block_info = block_info
        self.connected_blocks = []
        self.canvas = master  # Store reference to canvas
        
        # Configure block appearance
        self.configure(
            fg_color=block_info.get('color', '#4a4a4a'),
            corner_radius=10,
            border_width=2,
            border_color=block_info.get('border_color', '#666666')
        )
        
        # Create block content
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add block label
        self.label = ctk.CTkLabel(
            self.content_frame,
            text=block_type,
            text_color="white",
            font=("Arial", 12, "bold")
        )
        self.label.pack(side="left", padx=5)
        
        # Add parameters if any
        if block_info.get('params'):
            self.param_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.param_frame.pack(side="left", fill="x", expand=True)
            
            for param in block_info['params']:
                param_container = ctk.CTkFrame(self.param_frame, fg_color="#666666", corner_radius=5)
                param_container.pack(side="left", padx=2)
                
                param_entry = ctk.CTkEntry(
                    param_container,
                    width=50,
                    height=20,
                    fg_color="#444444",
                    border_color="#888888",
                    text_color="white"
                )
                param_entry.pack(padx=2, pady=2)
                setattr(self, f"param_{param}", param_entry)
        
        # Add connection points
        self.top_connector = ctk.CTkFrame(self, width=30, height=10, fg_color="#888888", corner_radius=5)
        self.top_connector.pack(fill="x", padx=10, pady=(2, 0))
        
        self.bottom_connector = ctk.CTkFrame(self, width=30, height=10, fg_color="#888888", corner_radius=5)
        self.bottom_connector.pack(fill="x", padx=10, pady=(0, 2))
        
        # Make the block draggable
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<B1-Motion>", self.drag)
        
        # Make all child widgets draggable
        for child in self.winfo_children():
            child.bind("<ButtonPress-1>", self.start_drag)
            child.bind("<ButtonRelease-1>", self.stop_drag)
            child.bind("<B1-Motion>", self.drag)
    
    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self.lift()  # Bring block to front
        self.configure(border_color="#00ff00")  # Highlight when dragging
    
    def stop_drag(self, event):
        self._drag_start_x = None
        self._drag_start_y = None
        self.configure(border_color=self.block_info.get('border_color', '#666666'))
    
    def drag(self, event):
        if hasattr(self, '_drag_start_x') and self._drag_start_x is not None:
            dx = event.x - self._drag_start_x
            dy = event.y - self._drag_start_y
            x = self.winfo_x() + dx
            y = self.winfo_y() + dy
            self.place(x=x, y=y)
            
            # Notify the game engine about the drag
            if hasattr(self.canvas, 'game_engine'):
                self.canvas.game_engine.check_snapping(self)

class SettingsWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Appearance settings
        self.create_appearance_settings()
        
        # Grid settings
        self.create_grid_settings()
        
        # Block settings
        self.create_block_settings()
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.main_frame,
            text="Save Settings",
            command=self.save_settings
        )
        self.save_button.pack(fill="x", padx=10, pady=10)
    
    def create_appearance_settings(self):
        # Appearance section
        appearance_frame = ctk.CTkFrame(self.main_frame)
        appearance_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(appearance_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=5)
        self.theme_combo = CTkComboBox(
            theme_frame,
            values=["System", "Dark", "Light"],
            command=self.change_theme
        )
        self.theme_combo.pack(side="left", padx=5)
        self.theme_combo.set(ctk.get_appearance_mode())
    
    def create_grid_settings(self):
        # Grid section
        grid_frame = ctk.CTkFrame(self.main_frame)
        grid_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            grid_frame,
            text="Grid Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Grid visibility
        self.grid_visible = ctk.CTkSwitch(
            grid_frame,
            text="Show Grid",
            command=self.toggle_grid
        )
        self.grid_visible.pack(anchor="w", padx=10, pady=5)
        self.grid_visible.select()  # Grid is visible by default
        
        # Grid size
        grid_size_frame = ctk.CTkFrame(grid_frame)
        grid_size_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(grid_size_frame, text="Grid Size:").pack(side="left", padx=5)
        self.grid_size_combo = CTkComboBox(
            grid_size_frame,
            values=["10", "20", "30", "40", "50"],
            command=self.change_grid_size
        )
        self.grid_size_combo.pack(side="left", padx=5)
        self.grid_size_combo.set("20")  # Default grid size
    
    def create_block_settings(self):
        # Block settings section
        block_frame = ctk.CTkFrame(self.main_frame)
        block_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            block_frame,
            text="Block Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Snap distance
        snap_frame = ctk.CTkFrame(block_frame)
        snap_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(snap_frame, text="Snap Distance:").pack(side="left", padx=5)
        self.snap_distance_combo = CTkComboBox(
            snap_frame,
            values=["20", "30", "40", "50"],
            command=self.change_snap_distance
        )
        self.snap_distance_combo.pack(side="left", padx=5)
        self.snap_distance_combo.set("30")  # Default snap distance
    
    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
    
    def toggle_grid(self):
        if hasattr(self.master, 'game_engine'):
            if self.grid_visible.get():
                self.master.game_engine.draw_grid()
            else:
                self.master.game_engine.canvas.delete("grid")
    
    def change_grid_size(self, size):
        if hasattr(self.master, 'game_engine'):
            self.master.game_engine.canvas.delete("grid")
            self.master.game_engine.draw_grid(int(size))
    
    def change_snap_distance(self, distance):
        if hasattr(self.master, 'game_engine'):
            self.master.game_engine.SNAP_DISTANCE = int(distance)
    
    def save_settings(self):
        # Save settings to a file
        settings = {
            'theme': self.theme_combo.get(),
            'grid_visible': self.grid_visible.get(),
            'grid_size': self.grid_size_combo.get(),
            'snap_distance': self.snap_distance_combo.get()
        }
        
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

class GameEngine:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.root = master
        self.master.title("FrogeeEngine")
        self.master.geometry("1367x768")
        
        # Initialize elements list
        self.elements = []
        self.selected_block = None
        
        # Initialize settings
        self.SNAP_DISTANCE = 30  # Default snap distance
        
        # Load settings if available
        self.load_settings()
        
        # Initialize block categories with Scratch-like blocks
        self.block_categories = {
            'Motion': {
                'move': {'code': 'move(%s) steps', 'params': ['steps'], 'color': '#4C97FF', 'border_color': '#3373CC'},
                'turn': {'code': 'turn(%s) degrees', 'params': ['degrees'], 'color': '#4C97FF', 'border_color': '#3373CC'},
                'go_to': {'code': 'go to x:%s y:%s', 'params': ['x', 'y'], 'color': '#4C97FF', 'border_color': '#3373CC'},
                'point': {'code': 'point in direction %s', 'params': ['direction'], 'color': '#4C97FF', 'border_color': '#3373CC'}
            },
            'Control': {
                'wait': {'code': 'wait %s seconds', 'params': ['seconds'], 'color': '#FFAB19', 'border_color': '#CF8B17'},
                'repeat': {'code': 'repeat %s times {\n    %s\n}', 'params': ['times', 'body'], 'color': '#FFAB19', 'border_color': '#CF8B17'},
                'forever': {'code': 'forever {\n    %s\n}', 'params': ['body'], 'color': '#FFAB19', 'border_color': '#CF8B17'},
                'if': {'code': 'if %s {\n    %s\n}', 'params': ['condition', 'body'], 'color': '#FFAB19', 'border_color': '#CF8B17'}
            },
            'Looks': {
                'say': {'code': 'say %s', 'params': ['text'], 'color': '#9966FF', 'border_color': '#774DCB'},
                'think': {'code': 'think %s', 'params': ['text'], 'color': '#9966FF', 'border_color': '#774DCB'},
                'change_size': {'code': 'change size by %s', 'params': ['size'], 'color': '#9966FF', 'border_color': '#774DCB'},
                'set_size': {'code': 'set size to %s%', 'params': ['size'], 'color': '#9966FF', 'border_color': '#774DCB'}
            },
            'Sound': {
                'play_sound': {'code': 'play sound %s', 'params': ['sound'], 'color': '#CF63CF', 'border_color': '#A63FA6'},
                'play_note': {'code': 'play note %s for %s beats', 'params': ['note', 'beats'], 'color': '#CF63CF', 'border_color': '#A63FA6'},
                'change_volume': {'code': 'change volume by %s', 'params': ['volume'], 'color': '#CF63CF', 'border_color': '#A63FA6'},
                'set_volume': {'code': 'set volume to %s%', 'params': ['volume'], 'color': '#CF63CF', 'border_color': '#A63FA6'}
            },
            'Operators': {
                'add': {'code': '%s + %s', 'params': ['a', 'b'], 'color': '#40BF4A', 'border_color': '#2E8A35'},
                'subtract': {'code': '%s - %s', 'params': ['a', 'b'], 'color': '#40BF4A', 'border_color': '#2E8A35'},
                'multiply': {'code': '%s * %s', 'params': ['a', 'b'], 'color': '#40BF4A', 'border_color': '#2E8A35'},
                'divide': {'code': '%s / %s', 'params': ['a', 'b'], 'color': '#40BF4A', 'border_color': '#2E8A35'}
            }
        }
        
        # Create layout
        self.create_layout()
        
        # Create block categories
        self.create_block_categories()

    def create_layout(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create toolbar
        self.toolbar = ctk.CTkFrame(self.main_frame, width=200)
        self.toolbar.pack(side="left", fill="y", padx=5, pady=5)
        
        # Create category tabs
        self.category_tabs = ctk.CTkTabview(self.toolbar)
        self.category_tabs.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas frame
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Create main canvas with grid
        self.canvas = tk.Canvas(self.canvas_frame, bg='#2b2b2b')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.game_engine = self  # Store reference to game engine
        
        # Set canvas scroll region
        self.canvas.configure(scrollregion=(0, 0, 2000, 2000))
        
        # Draw grid
        self.draw_grid()
        
        # Add toolbar buttons
        self.add_toolbar_buttons()
    
    def draw_grid(self, grid_size=20):
        # Remove existing grid
        self.canvas.delete("grid")
        
        # Draw vertical lines
        for x in range(0, 2000, grid_size):
            self.canvas.create_line(x, 0, x, 2000, fill='#333333', dash=(1, 2), tags="grid")
        
        # Draw horizontal lines
        for y in range(0, 2000, grid_size):
            self.canvas.create_line(0, y, 2000, y, fill='#333333', dash=(1, 2), tags="grid")
    
    def add_toolbar_buttons(self):
        # Add settings button
        self.settings_button = ctk.CTkButton(
            self.toolbar,
            text="Settings",
            command=self.open_settings
        )
        self.settings_button.pack(fill="x", padx=5, pady=5)
        
        # Add export button
        self.export_button = ctk.CTkButton(
            self.toolbar,
            text="Export to C",
            command=self.export_to_c
        )
        self.export_button.pack(fill="x", padx=5, pady=5)
        
        # Add clear button
        self.clear_button = ctk.CTkButton(
            self.toolbar,
            text="Clear All",
            command=self.clear_workspace
        )
        self.clear_button.pack(fill="x", padx=5, pady=5)
        
        # Add save/load buttons
        self.save_button = ctk.CTkButton(
            self.toolbar,
            text="Save Project",
            command=self.save_project
        )
        self.save_button.pack(fill="x", padx=5, pady=5)
        
        self.load_button = ctk.CTkButton(
            self.toolbar,
            text="Load Project",
            command=self.load_project
        )
        self.load_button.pack(fill="x", padx=5, pady=5)
        
        # Add run button
        self.run_button = ctk.CTkButton(
            self.toolbar,
            text="Run",
            command=self.run_project,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.run_button.pack(fill="x", padx=5, pady=5)
    
    def clear_workspace(self):
        for block in self.elements:
            self.canvas.delete(block.canvas_id)
            block.destroy()
        self.elements.clear()
    
    def save_project(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".fge",
            filetypes=[("Forgee Engine Project", "*.fge")]
        )
        if file_path:
            project_data = {
                'blocks': [],
                'connections': []
            }
            
            # Save blocks with their coordinates and parameters
            for i, block in enumerate(self.elements):
                block_data = {
                    'id': i,
                    'type': block.block_type,
                    'x': block.winfo_x(),
                    'y': block.winfo_y(),
                    'params': {}
                }
                
                # Save parameter values
                if block.block_info.get('params'):
                    for param in block.block_info['params']:
                        param_value = getattr(block, f"param_{param}").get()
                        block_data['params'][param] = param_value
                
                project_data['blocks'].append(block_data)
            
            # Save connections between blocks
            for i, block in enumerate(self.elements):
                for connected_block in block.connected_blocks:
                    # Only save each connection once
                    if self.elements.index(connected_block) > i:
                        connection = {
                            'from': i,
                            'to': self.elements.index(connected_block)
                        }
                        project_data['connections'].append(connection)
            
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=2)
            messagebox.showinfo("Success", "Project saved successfully!")
    
    def load_project(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Forgee Engine Project", "*.fge")]
        )
        if file_path:
            with open(file_path, 'r') as f:
                project_data = json.load(f)
            
            self.clear_workspace()
            
            # First create all blocks
            for block_data in project_data['blocks']:
                block_type = block_data['type']
                for category in self.block_categories.values():
                    if block_type in category:
                        block_info = category[block_type]
                        block = Block(self.canvas, block_type, block_info, width=150)
                        
                        # Set block position
                        block.place(x=block_data['x'], y=block_data['y'])
                        
                        # Set parameter values
                        if block_data.get('params'):
                            for param, value in block_data['params'].items():
                                param_entry = getattr(block, f"param_{param}")
                                param_entry.insert(0, value)
                        
                        # Make the block draggable
                        block.bind("<ButtonPress-1>", block.start_drag)
                        block.bind("<ButtonRelease-1>", block.stop_drag)
                        block.bind("<B1-Motion>", block.drag)
                        
                        self.elements.append(block)
            
            # Then restore connections
            for connection in project_data.get('connections', []):
                from_block = self.elements[connection['from']]
                to_block = self.elements[connection['to']]
                
                # Add connection to both blocks
                from_block.connected_blocks.append(to_block)
                to_block.connected_blocks.append(from_block)
                
                # Draw connection line
                self.draw_connection_line(from_block, to_block)
            
            messagebox.showinfo("Success", "Project loaded successfully!")

    def create_buttons(self):
        for block_name, block_info in self.blocks.items():
            button = ctk.CTkButton(self.button_frame, text=block_name, command=lambda block_name=block_name: self.create_block(block_name))
            button.pack(fill="x", pady =10 )

    def create_block(self, block_name, block_info):
        # Create the block directly on the canvas
        block = Block(self.canvas, block_name, block_info, width=150)
        
        # Calculate position to add the block
        x = self.canvas.canvasx(0) + 50
        y = self.canvas.canvasy(0) + 50
        
        # Add the block to the canvas
        canvas_id = self.canvas.create_window(x, y, window=block, tags=f"block_{block_name}")
        block.canvas_id = canvas_id
        
        # Make the block draggable
        block.bind("<ButtonPress-1>", self.start_drag)
        block.bind("<ButtonRelease-1>", self.stop_drag)
        block.bind("<B1-Motion>", self.drag)
        
        # Store the block
        self.elements.append(block)
        
        return block

    def create_block_categories(self):
        # Create tabs for each category
        for category in self.block_categories.keys():
            tab = self.category_tabs.add(category)
            
            # Create a frame for the blocks in this category
            block_frame = ctk.CTkFrame(tab)
            block_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add blocks to the category
            for block_name, block_info in self.block_categories[category].items():
                button = ctk.CTkButton(
                    block_frame,
                    text=block_name,
                    fg_color=block_info.get('color', '#4a4a4a'),
                    command=lambda bn=block_name, bi=block_info: self.create_block(bn, bi)
                )
                button.pack(fill="x", padx=5, pady=2)
    
    def export_to_c(self):
        # Validate blocks before export
        errors = self.validate_blocks()
        if errors:
            error_message = "Cannot export code due to the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Export Error", error_message)
            return
        
        # Generate C code
        code = []
        visited = set()
        
        def traverse_block(block, indent=0):
            if block in visited:
                return
            visited.add(block)
            
            # Get block parameters
            params = []
            if block.block_info.get('params'):
                for param in block.block_info['params']:
                    param_value = getattr(block, f"param_{param}").get()
                    # Convert string parameters to proper C format
                    if param in ['text', 'sound']:
                        param_value = f'"{param_value}"'
                    params.append(param_value)
            
            # Convert block code to C
            block_code = self.convert_to_c(block.block_type, block.block_info['code'], params)
            
            # Add proper indentation
            indented_code = "    " * indent + block_code
            
            # Split code into lines and add to output
            for line in indented_code.split('\n'):
                code.append(line)
            
            # Traverse connected blocks with increased indentation
            for connected_block in block.connected_blocks:
                traverse_block(connected_block, indent + 1)
        
        # Start from blocks that aren't connected to any other blocks
        for block in self.elements:
            if not any(block in other.connected_blocks for other in self.elements):
                traverse_block(block)
        
        # Create the complete C program
        c_program = [
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <unistd.h>",
            "#include <math.h>",
            "",
            "// Global variables",
            "int current_x = 0;",
            "int current_y = 0;",
            "int current_direction = 0;",
            "int current_size = 100;",
            "int current_volume = 100;",
            "",
            "// Function declarations",
            "void move(int steps);",
            "void turn(int degrees);",
            "void go_to(int x, int y);",
            "void point_direction(int direction);",
            "void say(const char* text);",
            "void think(const char* text);",
            "void change_size(int size);",
            "void set_size(int size);",
            "void play_sound(const char* sound);",
            "void play_note(int note, int beats);",
            "void change_volume(int volume);",
            "void set_volume(int volume);",
            "void wait(int seconds);",
            "",
            "int main() {",
            "    printf(\"Starting program...\\n\");",
        ]
        
        # Add the generated code with proper indentation
        for line in code:
            c_program.append("    " + line)
        
        c_program.extend([
            "    printf(\"\\nProgram finished.\\n\");",
            "    return 0;",
            "}",
            "",
            "// Function implementations",
            "void move(int steps) {",
            "    double radians = current_direction * M_PI / 180.0;",
            "    current_x += steps * cos(radians);",
            "    current_y += steps * sin(radians);",
            "    printf(\"Moving %d steps to position (%d, %d)\\n\", steps, current_x, current_y);",
            "}",
            "",
            "void turn(int degrees) {",
            "    current_direction = (current_direction + degrees) % 360;",
            "    printf(\"Turning %d degrees to direction %d\\n\", degrees, current_direction);",
            "}",
            "",
            "void go_to(int x, int y) {",
            "    current_x = x;",
            "    current_y = y;",
            "    printf(\"Going to position (%d, %d)\\n\", x, y);",
            "}",
            "",
            "void point_direction(int direction) {",
            "    current_direction = direction % 360;",
            "    printf(\"Pointing in direction %d\\n\", direction);",
            "}",
            "",
            "void say(const char* text) {",
            "    printf(\"Saying: %s\\n\", text);",
            "}",
            "",
            "void think(const char* text) {",
            "    printf(\"Thinking: %s\\n\", text);",
            "}",
            "",
            "void change_size(int size) {",
            "    current_size += size;",
            "    printf(\"Changing size by %d to %d%%\\n\", size, current_size);",
            "}",
            "",
            "void set_size(int size) {",
            "    current_size = size;",
            "    printf(\"Setting size to %d%%\\n\", size);",
            "}",
            "",
            "void play_sound(const char* sound) {",
            "    printf(\"Playing sound: %s\\n\", sound);",
            "}",
            "",
            "void play_note(int note, int beats) {",
            "    printf(\"Playing note %d for %d beats\\n\", note, beats);",
            "}",
            "",
            "void change_volume(int volume) {",
            "    current_volume += volume;",
            "    if (current_volume > 100) current_volume = 100;",
            "    if (current_volume < 0) current_volume = 0;",
            "    printf(\"Changing volume by %d to %d%%\\n\", volume, current_volume);",
            "}",
            "",
            "void set_volume(int volume) {",
            "    current_volume = volume;",
            "    if (current_volume > 100) current_volume = 100;",
            "    if (current_volume < 0) current_volume = 0;",
            "    printf(\"Setting volume to %d%%\\n\", current_volume);",
            "}",
            "",
            "void wait(int seconds) {",
            "    printf(\"Waiting %d seconds...\\n\", seconds);",
            "    sleep(seconds);",
            "}"
        ])
        
        # Save to file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[('C Source File', '*.c')]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(c_program))
            messagebox.showinfo("Success", "C code exported successfully!")

    def convert_to_c(self, block_type, block_code, params):
        # Convert block code to C syntax
        if block_type == 'move':
            return f"move({params[0]});"
        elif block_type == 'turn':
            return f"turn({params[0]});"
        elif block_type == 'go_to':
            return f"go_to({params[0]}, {params[1]});"
        elif block_type == 'point':
            return f"point_direction({params[0]});"
        elif block_type == 'say':
            return f"say({params[0]});"
        elif block_type == 'think':
            return f"think({params[0]});"
        elif block_type == 'change_size':
            return f"change_size({params[0]});"
        elif block_type == 'set_size':
            return f"set_size({params[0]});"
        elif block_type == 'play_sound':
            return f"play_sound({params[0]});"
        elif block_type == 'play_note':
            return f"play_note({params[0]}, {params[1]});"
        elif block_type == 'change_volume':
            return f"change_volume({params[0]});"
        elif block_type == 'set_volume':
            return f"set_volume({params[0]});"
        elif block_type == 'wait':
            return f"wait({params[0]});"
        elif block_type == 'repeat':
            return f"for(int i = 0; i < {params[0]}; i++) {{\n    {params[1]}\n}}"
        elif block_type == 'forever':
            return f"while(1) {{\n    {params[0]}\n}}"
        elif block_type == 'if':
            return f"if({params[0]}) {{\n    {params[1]}\n}}"
        elif block_type in ['add', 'subtract', 'multiply', 'divide']:
            op = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}[block_type]
            return f"({params[0]} {op} {params[1]})"
        else:
            return block_code % tuple(params)
    
    def validate_blocks(self):
        errors = []
        
        # Check for disconnected blocks
        for block in self.elements:
            if not block.connected_blocks and not any(block in other.connected_blocks for other in self.elements):
                errors.append(f"Block '{block.block_type}' is not connected to any other block")
        
        # Check for required parameters
        for block in self.elements:
            if block.block_info.get('params'):
                for param in block.block_info['params']:
                    param_value = getattr(block, f"param_{param}").get()
                    if not param_value:
                        errors.append(f"Block '{block.block_type}' is missing required parameter '{param}'")
        
        return errors
    
    def run_project(self):
        # Validate blocks before running
        errors = self.validate_blocks()
        if errors:
            error_message = "Cannot run project due to the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Run Error", error_message)
            return
        
        # Generate and execute code
        code = self.export_to_code()
        try:
            # Create a new window to show the execution
            execution_window = ctk.CTkToplevel(self.master)
            execution_window.title("Project Execution")
            execution_window.geometry("400x300")
            
            # Add a text area to show output
            output_area = ctk.CTkTextbox(execution_window)
            output_area.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Execute the code and show output
            output_area.insert("1.0", "Running project...\n\n")
            output_area.insert("end", code)
            
        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def check_snapping(self, dragged_block):
        if not dragged_block:
            return
            
        dragged_coords = (dragged_block.winfo_x(), dragged_block.winfo_y())
        dragged_bottom = dragged_coords[1] + dragged_block.winfo_height()
        dragged_center_x = dragged_coords[0] + (dragged_block.winfo_width() / 2)
        
        # Grid size for snapping
        GRID_SIZE = 20
        SNAP_DISTANCE = 30  # Distance at which blocks will snap together
        
        # Find the closest block to snap to
        closest_block = None
        min_distance = float('inf')
        
        for block in self.elements:
            if block != dragged_block:
                block_coords = (block.winfo_x(), block.winfo_y())
                block_top = block_coords[1]
                block_center_x = block_coords[0] + (block.winfo_width() / 2)
                
                # Calculate distances
                vertical_distance = abs(dragged_bottom - block_top)
                horizontal_distance = abs(dragged_center_x - block_center_x)
                
                # Check if blocks are close enough to snap
                if (vertical_distance < SNAP_DISTANCE and 
                    horizontal_distance < SNAP_DISTANCE and 
                    vertical_distance < min_distance):
                    min_distance = vertical_distance
                    closest_block = block
        
        if closest_block:
            # Snap the blocks together
            block_coords = (closest_block.winfo_x(), closest_block.winfo_y())
            
            # Align horizontally with the block above
            dragged_block.place(
                x=block_coords[0],  # Same X position as the block above
                y=block_coords[1] - dragged_block.winfo_height()  # Place directly under
            )
            
            # Connect the blocks if not already connected
            if closest_block not in dragged_block.connected_blocks:
                # Remove any existing connections for the dragged block
                for block in self.elements:
                    if dragged_block in block.connected_blocks:
                        block.connected_blocks.remove(dragged_block)
                dragged_block.connected_blocks.clear()
                
                # Add new connection
                dragged_block.connected_blocks.append(closest_block)
                closest_block.connected_blocks.append(dragged_block)
                
                # Visual feedback for connection
                dragged_block.configure(border_color="#00ff00")
                closest_block.configure(border_color="#00ff00")
                
                # Draw connection line
                self.draw_connection_line(closest_block, dragged_block)

    def draw_connection_line(self, block1, block2):
        # Remove any existing connection lines
        for tag in self.canvas.find_withtag("connection"):
            self.canvas.delete(tag)
        
        # Get coordinates for both blocks
        coords1 = (block1.winfo_x(), block1.winfo_y())
        coords2 = (block2.winfo_x(), block2.winfo_y())
        
        # Calculate connection points
        x1 = coords1[0] + block1.winfo_width() / 2
        y1 = coords1[1] + block1.winfo_height()
        x2 = coords2[0] + block2.winfo_width() / 2
        y2 = coords2[1]
        
        # Draw the connection line
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill="#00ff00",
            width=2,
            dash=(4, 4),
            tags="connection"
        )

    def open_settings(self):
        settings_window = SettingsWindow(self.master)
        settings_window.focus_set()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                
                # Apply theme
                if 'theme' in settings:
                    ctk.set_appearance_mode(settings['theme'])
                
                # Store other settings
                self.SNAP_DISTANCE = int(settings.get('snap_distance', 30))
                
        except FileNotFoundError:
            # Use default settings if file doesn't exist
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")

if __name__ == "__main__":
    app = ctk.CTk()
    game_engine = GameEngine(app)
    app.mainloop()