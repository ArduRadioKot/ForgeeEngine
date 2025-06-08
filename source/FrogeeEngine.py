import customtkinter as ctk
from tkinter import simpledialog, filedialog, messagebox
from customtkinter import CTk, CTkLabel, CTkButton, CTkToplevel, CTkSwitch, CTkComboBox
import tkinter as tk
from PIL import Image, ImageTk
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Block(ctk.CTkFrame):
    def __init__(self, master, block_type, block_info, **kwargs):
        super().__init__(master, **kwargs)
        self.block_type = block_type
        self.block_info = block_info
        self.connected_blocks = []
        self.canvas = master
        self.is_selected = False
        
        self.configure(
            fg_color=block_info.get('color', '#4a4a4a'),
            corner_radius=10,
            border_width=2,
            border_color=block_info.get('border_color', '#666666')
        )
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.label = ctk.CTkLabel(
            self.content_frame,
            text=block_type,
            text_color="white",
            font=("Arial", 12, "bold")
        )
        self.label.pack(side="left", padx=5)
        
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
        
        self.top_connector = ctk.CTkFrame(self, width=30, height=10, fg_color="#888888", corner_radius=5)
        self.top_connector.pack(fill="x", padx=10, pady=(2, 0))
        
        self.bottom_connector = ctk.CTkFrame(self, width=30, height=10, fg_color="#888888", corner_radius=5)
        self.bottom_connector.pack(fill="x", padx=10, pady=(0, 2))
        
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Button-3>", self.show_context_menu)
        self.bind("<Delete>", self.delete_block)
        
        for child in self.winfo_children():
            child.bind("<ButtonPress-1>", self.start_drag)
            child.bind("<ButtonRelease-1>", self.stop_drag)
            child.bind("<B1-Motion>", self.drag)
            child.bind("<Button-3>", self.show_context_menu)
            child.bind("<Delete>", self.delete_block)
    
    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self.lift()
        self.select_block()
    
    def select_block(self):
        if hasattr(self.canvas, 'game_engine'):
            for block in self.canvas.game_engine.elements:
                if block != self:
                    block.deselect_block()
        
        self.is_selected = True
        self.configure(border_color="#00ff00", border_width=3)
        
        if hasattr(self.canvas, 'game_engine'):
            self.canvas.game_engine.selected_block = self
    
    def deselect_block(self):
        self.is_selected = False
        self.configure(border_color=self.block_info.get('border_color', '#666666'), border_width=2)
    
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
            
            if hasattr(self.canvas, 'game_engine'):
                self.canvas.game_engine.check_snapping(self)
    
    def show_context_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Delete Block", command=self.delete_block)
        context_menu.add_command(label="Duplicate Block", command=self.duplicate_block)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def delete_block(self, event=None):
        if hasattr(self.canvas, 'game_engine'):
            for connected_block in self.connected_blocks[:]:
                if self in connected_block.connected_blocks:
                    connected_block.connected_blocks.remove(self)
            
            if hasattr(self, 'canvas_id'):
                self.canvas.delete(self.canvas_id)
            
            if self in self.canvas.game_engine.elements:
                self.canvas.game_engine.elements.remove(self)
            
            if self.canvas.game_engine.selected_block == self:
                self.canvas.game_engine.selected_block = None
            
            self.destroy()
            self.canvas.game_engine.redraw_connections()
    
    def duplicate_block(self):
        if hasattr(self.canvas, 'game_engine'):
            new_block = Block(self.canvas, self.block_type, self.block_info, width=150)
            
            if self.block_info.get('params'):
                for param in self.block_info['params']:
                    old_value = getattr(self, f"param_{param}").get()
                    new_entry = getattr(new_block, f"param_{param}")
                    new_entry.insert(0, old_value)
            
            x = self.winfo_x() + 20
            y = self.winfo_y() + 20
            
            canvas_id = self.canvas.create_window(x, y, window=new_block, tags=f"block_{self.block_type}")
            new_block.canvas_id = canvas_id
            
            self.canvas.game_engine.elements.append(new_block)


class SettingsWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_appearance_settings()
        self.create_grid_settings()
        self.create_block_settings()
        
        self.save_button = ctk.CTkButton(
            self.main_frame,
            text="Save Settings",
            command=self.save_settings
        )
        self.save_button.pack(fill="x", padx=10, pady=10)
    
    def create_appearance_settings(self):
        appearance_frame = ctk.CTkFrame(self.main_frame)
        appearance_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
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
        grid_frame = ctk.CTkFrame(self.main_frame)
        grid_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            grid_frame,
            text="Grid Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.grid_visible = ctk.CTkSwitch(
            grid_frame,
            text="Show Grid",
            command=self.toggle_grid
        )
        self.grid_visible.pack(anchor="w", padx=10, pady=5)
        self.grid_visible.select()
        
        grid_size_frame = ctk.CTkFrame(grid_frame)
        grid_size_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(grid_size_frame, text="Grid Size:").pack(side="left", padx=5)
        self.grid_size_combo = CTkComboBox(
            grid_size_frame,
            values=["10", "20", "30", "40", "50"],
            command=self.change_grid_size
        )
        self.grid_size_combo.pack(side="left", padx=5)
        self.grid_size_combo.set("20")
    
    def create_block_settings(self):
        block_frame = ctk.CTkFrame(self.main_frame)
        block_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            block_frame,
            text="Block Settings",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        snap_frame = ctk.CTkFrame(block_frame)
        snap_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(snap_frame, text="Snap Distance:").pack(side="left", padx=5)
        self.snap_distance_combo = CTkComboBox(
            snap_frame,
            values=["20", "30", "40", "50"],
            command=self.change_snap_distance
        )
        self.snap_distance_combo.pack(side="left", padx=5)
        self.snap_distance_combo.set("30")
    
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

class PaintEngine:
    def __init__(self, master):
        self.root = ctk.CTk()
        self.master = master
        self.root.title("Bitmap Editor")
        self.root.geometry("800x640")

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self.canvas = ctk.CTkCanvas(
            self.canvas_frame,
            width=512,
            height=256,
            background="#ffffff",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=10)
        
        self.pixel_size = 4
        self.pixels = {}
        self.initialize_canvas()

        self.brush_size = 1
        self.eraser_size = 1

        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.pack(fill="x", pady=(0, 20))
        
        self.brush_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.brush_frame.pack(fill="x", pady=5)
        
        self.brush_label = ctk.CTkLabel(
            self.brush_frame,
            text="Brush Size",
            font=("Arial", 12, "bold")
        )
        self.brush_label.pack(side="left", padx=10)
        
        self.brush_slider = ctk.CTkSlider(
            self.brush_frame,
            from_=1,
            to=10,
            width=200,
            command=self.update_brush_size,
            button_color="#40BF4A",
            button_hover_color="#2E8A35",
            progress_color="#40BF4A"
        )
        self.brush_slider.pack(side="left", padx=10)
        
        self.brush_value = ctk.CTkLabel(
            self.brush_frame,
            text="1",
            font=("Arial", 12)
        )
        self.brush_value.pack(side="left", padx=10)
        
        self.eraser_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.eraser_frame.pack(fill="x", pady=5)
        
        self.eraser_label = ctk.CTkLabel(
            self.eraser_frame,
            text="Eraser Size",
            font=("Arial", 12, "bold")
        )
        self.eraser_label.pack(side="left", padx=10)
        
        self.eraser_slider = ctk.CTkSlider(
            self.eraser_frame,
            from_=1,
            to=10,
            width=200,
            command=self.update_eraser_size,
            button_color="#40BF4A",
            button_hover_color="#2E8A35",
            progress_color="#40BF4A"
        )
        self.eraser_slider.pack(side="left", padx=10)
        
        self.eraser_value = ctk.CTkLabel(
            self.eraser_frame,
            text="1",
            font=("Arial", 12)
        )
        self.eraser_value.pack(side="left", padx=10)
        
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=(0, 20))
        
        self.save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Save Bitmap",
            font=("Arial", 12, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.save_bitmap_h
        )
        self.save_button.pack(side="left", padx=5)
        
        self.open_button = ctk.CTkButton(
            self.buttons_frame,
            text="Open Image",
            font=("Arial", 12, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.open_image
        )
        self.open_button.pack(side="left", padx=5)
        
        self.quit_button = ctk.CTkButton(
            self.buttons_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            height=35,
            corner_radius=8,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.quit
        )
        self.quit_button.pack(side="right", padx=5)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<B3-Motion>", self.erase)
        self.image = None
    
    def initialize_canvas(self):
        for i in range(64):
            for j in range(128):
                x1 = j * self.pixel_size
                y1 = i * self.pixel_size
                x2 = x1 + self.pixel_size
                y2 = y1 + self.pixel_size
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="white",
                    outline="#e0e0e0",
                    tags=f"pixel_{i}_{j}"
                )
                self.pixels[(i, j)] = rect_id
    
    def quit(self):
        self.root.destroy()

    def paint_pixel(self, x, y, color, brush_size):
        for i in range(-brush_size, brush_size+1):
            for j in range(-brush_size, brush_size+1):
                new_x = x + i
                new_y = y + j
                if 0 <= new_x < 128 and 0 <= new_y < 64:
                    pixel_id = self.pixels.get((new_y, new_x))
                    if pixel_id:
                        self.canvas.itemconfig(pixel_id, fill=color)

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
        for i in range(64):
            byte = 0
            for j in range(128):
                pixel_id = self.pixels.get((i, j))
                if pixel_id:
                    pixel_color = self.canvas.itemcget(pixel_id, "fill")
                if pixel_color == "black":
                        byte |= 1 << (7 - (j % 8))
                if j % 8 == 7:
                    bitmap.append(f"0x{byte:02x}")
                    byte = 0
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".h",
            filetypes=[("Header files", "*.h")],
            initialfile="bitmap.h"
        )
        
        if file_path:
            with open(file_path, "w") as f:
                f.write("const uint8_t bitmap[] = {\n")
                for i in range(0, len(bitmap), 16):
                    f.write(", ".join(bitmap[i:i+16]) + ",\n")
                f.write("};\n")

    def update_brush_size(self, value):
        self.brush_size = int(value)
        self.brush_value.configure(text=str(self.brush_size))

    def update_eraser_size(self, value):
        self.eraser_size = int(value)
        self.eraser_value.configure(text=str(self.eraser_size))

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.bmp")]
        )
        if file_path:
            image = Image.open(file_path)
            image = image.resize((128, 64))
            pixels = image.load()
            
            for i in range(64):
                for j in range(128):
                    pixel_id = self.pixels.get((i, j))
                    if pixel_id:
                        r, g, b = pixels[j, i][:3]
                        color = "black" if (r + g + b) < 384 else "white"
                        self.canvas.itemconfig(pixel_id, fill=color)

    def run(self):
        self.root.mainloop()

class TextIde(ctk.CTk):
    def __init__(self, master=None, game_engine=None):
        super().__init__()

        self.title("Code Editor")
        self.geometry("1000x700")
        self.game_engine = game_engine
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create toolbar
        self.toolbar = ctk.CTkFrame(self)
        self.toolbar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add toolbar buttons
        self.add_toolbar_buttons()
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Create text area with line numbers
        self.create_text_area()
        
        # Configure syntax highlighting
        self.configure_syntax_highlighting()
        
        # Bind events
        self.text_area.bind("<KeyRelease>", self.highlight_syntax_realtime)  
        
        # Update line numbers periodically
        self.update_line_numbers()

    def add_toolbar_buttons(self):
        # Save button
        self.save_button = ctk.CTkButton(
            self.toolbar,
            text="Save",
            command=self.save_file,
            width=120
        )
        self.save_button.pack(padx=5, pady=5)
        
        # Load button
        self.load_button = ctk.CTkButton(
            self.toolbar,
            text="Load",
            command=self.load_file,
            width=120
        )
        self.load_button.pack(padx=5, pady=5)
        
        # Update from blocks button
        if self.game_engine:
            self.update_button = ctk.CTkButton(
                self.toolbar,
                text="Update from Blocks",
                command=self.update_from_blocks,
                width=120
            )
            self.update_button.pack(padx=5, pady=5)
        
        # Theme selector
        self.theme_label = ctk.CTkLabel(self.toolbar, text="Theme:")
        self.theme_label.pack(padx=5, pady=(20, 5))
        
        self.theme_combo = ctk.CTkComboBox(
            self.toolbar,
            values=["System", "Dark", "Light"],
            command=self.change_theme,
            width=120
        )
        self.theme_combo.pack(padx=5, pady=5)
        self.theme_combo.set(ctk.get_appearance_mode())
        
        # Font size selector
        self.font_label = ctk.CTkLabel(self.toolbar, text="Font Size:")
        self.font_label.pack(padx=5, pady=(20, 5))
        
        self.font_combo = ctk.CTkComboBox(
            self.toolbar,
            values=["10", "12", "14", "16", "18"],
            command=self.change_font_size,
            width=120
        )
        self.font_combo.pack(padx=5, pady=5)
        self.font_combo.set("12")

    def create_text_area(self):
        # Create frame for text area and line numbers
        self.text_frame = ctk.CTkFrame(self.main_frame)
        self.text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create line numbers area
        self.line_numbers = tk.Text(
            self.text_frame,
            width=4,
            padx=3,
            takefocus=0,
            border=0,
            background='#2b2b2b',
            foreground='#666666',
            font=('Consolas', 12)
        )
        self.line_numbers.pack(side="left", fill="y")
        
        # Create text area
        self.text_area = tk.Text(
            self.text_frame,
            wrap="none",
            font=('Consolas', 12),
            background='#2b2b2b',
            foreground='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#404040',
            selectforeground='#ffffff',
            padx=5,
            pady=5
        )
        self.text_area.pack(side="left", fill="both", expand=True)
        
        # Add scrollbars
        self.v_scrollbar = ctk.CTkScrollbar(self.text_frame, command=self.text_area.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.text_area.configure(yscrollcommand=self.v_scrollbar.set)
        
        self.h_scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="horizontal", command=self.text_area.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.text_area.configure(xscrollcommand=self.h_scrollbar.set)

    def configure_syntax_highlighting(self):
        # Configure syntax highlighting tags
        self.text_area.tag_configure('keyword', foreground='#569CD6')
        self.text_area.tag_configure('string', foreground='#CE9178')
        self.text_area.tag_configure('comment', foreground='#6A9955')
        self.text_area.tag_configure('function', foreground='#DCDCAA')
        self.text_area.tag_configure('class', foreground='#4EC9B0')
        self.text_area.tag_configure('number', foreground='#B5CEA8')
        self.text_area.tag_configure('operator', foreground='#D4D4D4')
        
        # Define keywords and patterns
        self.keywords = [
            'if', 'else', 'elif', 'while', 'for', 'in', 'def', 'class',
            'return', 'break', 'continue', 'pass', 'import', 'from', 'as',
            'try', 'except', 'finally', 'raise', 'with', 'global', 'nonlocal',
            'True', 'False', 'None', 'and', 'or', 'not', 'is', 'lambda'
        ]
        
        self.operators = [
            '+', '-', '*', '/', '//', '%', '**', '=', '+=', '-=', '*=',
            '/=', '//=', '%=', '**=', '==', '!=', '<', '>', '<=', '>=',
            '&', '|', '^', '~', '<<', '>>', 'and', 'or', 'not', 'is', 'in'
        ]

    def update_line_numbers(self):
        # Update line numbers
        line_count = self.text_area.get('1.0', 'end-1c').count('\n') + 1
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_text)
        
        # Schedule next update
        self.after(100, self.update_line_numbers)

    def highlight_syntax_realtime(self, event=None):
        # Remove all existing tags
        for tag in ['keyword', 'string', 'comment', 'function', 'class', 'number', 'operator']:
            self.text_area.tag_remove(tag, '1.0', 'end')
        
        # Get the text content
        content = self.text_area.get('1.0', 'end-1c')
        lines = content.split('\n')
        
        # Process each line
        for i, line in enumerate(lines, 1):
            # Highlight keywords
            for keyword in self.keywords:
                self.highlight_word(keyword, i, 'keyword')
            
            # Highlight operators
            for operator in self.operators:
                self.highlight_word(operator, i, 'operator')
            
            # Highlight strings
            start = 0
            while True:
                start = line.find('"', start)
                if start == -1:
                    break
                end = line.find('"', start + 1)
                if end == -1:
                    break
                self.text_area.tag_add('string', f'{i}.{start}', f'{i}.{end + 1}')
                start = end + 1
            
            # Highlight comments
            comment_start = line.find('#')
            if comment_start != -1:
                self.text_area.tag_add('comment', f'{i}.{comment_start}', f'{i}.end')
            
            # Highlight numbers
            import re
            for match in re.finditer(r'\b\d+\b', line):
                start, end = match.span()
                self.text_area.tag_add('number', f'{i}.{start}', f'{i}.{end}')

    def highlight_word(self, word, line, tag):
        start = f'{line}.{self.text_area.get(f"{line}.0", f"{line}.end").index(word)}'
        end = f'{line}.{self.text_area.get(f"{line}.0", f"{line}.end").index(word) + len(word)}'
        self.text_area.tag_add(tag, start, end)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.text_area.get('1.0', 'end-1c'))
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.text_area.delete('1.0', 'end')
                    self.text_area.insert('1.0', f.read())
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def update_from_blocks(self):
        if self.game_engine:
            # Get the generated code from blocks
            code = self.game_engine.export_to_code()
            # Update text area
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('1.0', code)

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
        if theme == "Dark":
            self.text_area.configure(background='#2b2b2b', foreground='#ffffff')
            self.line_numbers.configure(background='#2b2b2b', foreground='#666666')
        else:
            self.text_area.configure(background='#ffffff', foreground='#000000')
            self.line_numbers.configure(background='#f0f0f0', foreground='#666666')

    def change_font_size(self, size):
        self.text_area.configure(font=('Consolas', int(size)))
        self.line_numbers.configure(font=('Consolas', int(size)))

    def run(self):
        self.mainloop()

class GameEngine:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.root = master
        self.master.title("FrogeeEngine")
        self.master.geometry("1367x768")
        
        self.elements = []
        self.selected_block = None
        self.SNAP_DISTANCE = 30
        
        self.load_settings()
        
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
            },
            'Graphics': {
                'bitmap': {'code': 'display_bitmap(%s)', 'params': ['bitmap_name'], 'color': '#FF5252', 'border_color': '#CC4040'}
            }
        }
        
        self.create_layout()
        self.create_block_categories()
        
        self.master.bind("<Delete>", self.delete_selected_block)
        self.canvas.bind("<Button-1>", self.deselect_all_blocks)

    def create_layout(self):
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill="both", expand=True)
        
        self.toolbar = ctk.CTkFrame(self.main_frame, width=200)
        self.toolbar.pack(side="left", fill="y", padx=5, pady=5)
        
        self.category_tabs = ctk.CTkTabview(self.toolbar)
        self.category_tabs.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg='#2b2b2b')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.game_engine = self
        
        self.canvas.configure(scrollregion=(0, 0, 2000, 2000))
        
        self.draw_grid()
        self.add_toolbar_buttons()
    
    def draw_grid(self, grid_size=20):
        self.canvas.delete("grid")
        
        for x in range(0, 2000, grid_size):
            self.canvas.create_line(x, 0, x, 2000, fill='#333333', dash=(1, 2), tags="grid")
        
        for y in range(0, 2000, grid_size):
            self.canvas.create_line(0, y, 2000, y, fill='#333333', dash=(1, 2), tags="grid")
    
    def add_toolbar_buttons(self):
        self.settings_button = ctk.CTkButton(
            self.toolbar,
            text="Settings",
            command=self.open_settings
        )
        self.settings_button.pack(fill="x", padx=5, pady=5)
        
        self.editor_button = ctk.CTkButton(
            self.toolbar,
            text="Open Code Editor",
            command=self.open_text_editor
        )
        self.editor_button.pack(fill="x", padx=5, pady=5)
        
        self.bitmap_editor_button = ctk.CTkButton(
            self.toolbar,
            text="Open Bitmap Editor",
            command=self.open_bitmap_editor
        )
        self.bitmap_editor_button.pack(fill="x", padx=5, pady=5)
        
        self.export_button = ctk.CTkButton(
            self.toolbar,
            text="Export to C",
            command=self.export_to_c
        )
        self.export_button.pack(fill="x", padx=5, pady=5)
        
        self.clear_button = ctk.CTkButton(
            self.toolbar,
            text="Clear All",
            command=self.clear_workspace
        )
        self.clear_button.pack(fill="x", padx=5, pady=5)
        
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
            
            for i, block in enumerate(self.elements):
                block_data = {
                    'id': i,
                    'type': block.block_type,
                    'x': block.winfo_x(),
                    'y': block.winfo_y(),
                    'params': {}
                }
                
                if block.block_info.get('params'):
                    for param in block.block_info['params']:
                        param_value = getattr(block, f"param_{param}").get()
                        block_data['params'][param] = param_value
                
                project_data['blocks'].append(block_data)
            
            for i, block in enumerate(self.elements):
                for connected_block in block.connected_blocks:
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
            
            for block_data in project_data['blocks']:
                block_type = block_data['type']
                for category in self.block_categories.values():
                    if block_type in category:
                        block_info = category[block_type]
                        block = Block(self.canvas, block_type, block_info, width=150)
                        
                        block.place(x=block_data['x'], y=block_data['y'])
                        
                        if block_data.get('params'):
                            for param, value in block_data['params'].items():
                                param_entry = getattr(block, f"param_{param}")
                                param_entry.insert(0, value)
                        
                        block.bind("<ButtonPress-1>", block.start_drag)
                        block.bind("<ButtonRelease-1>", block.stop_drag)
                        block.bind("<B1-Motion>", block.drag)
                        
                        self.elements.append(block)
            
            for connection in project_data.get('connections', []):
                from_block = self.elements[connection['from']]
                to_block = self.elements[connection['to']]
                
                from_block.connected_blocks.append(to_block)
                to_block.connected_blocks.append(from_block)
                
                self.draw_connection_line(from_block, to_block)
            
            messagebox.showinfo("Success", "Project loaded successfully!")

    def create_block(self, block_name, block_info):
        block = Block(self.canvas, block_name, block_info, width=150)
        
        x = self.canvas.canvasx(0) + 50
        y = self.canvas.canvasy(0) + 50
        
        canvas_id = self.canvas.create_window(x, y, window=block, tags=f"block_{block_name}")
        block.canvas_id = canvas_id
        
        block.bind("<ButtonPress-1>", block.start_drag)
        block.bind("<ButtonRelease-1>", block.stop_drag)
        block.bind("<B1-Motion>", block.drag)
        block.bind("<Button-3>", block.show_context_menu)
        block.bind("<Delete>", block.delete_block)
        
        self.elements.append(block)
        block.select_block()
        
        return block

    def create_block_categories(self):
        for category in self.block_categories.keys():
            tab = self.category_tabs.add(category)
            
            block_frame = ctk.CTkFrame(tab)
            block_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            for block_name, block_info in self.block_categories[category].items():
                button = ctk.CTkButton(
                    block_frame,
                    text=block_name,
                    fg_color=block_info.get('color', '#4a4a4a'),
                    command=lambda bn=block_name, bi=block_info: self.create_block(bn, bi)
                )
                button.pack(fill="x", padx=5, pady=2)
    
    def export_to_c(self):
        errors = self.validate_blocks()
        if errors:
            error_message = "Cannot export code due to the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Export Error", error_message)
            return
        
        code = []
        visited = set()
        
        def traverse_block(block, indent=0):
            if block in visited:
                return
            visited.add(block)
            
            params = []
            if block.block_info.get('params'):
                for param in block.block_info['params']:
                    param_value = getattr(block, f"param_{param}").get()
                    if param in ['text', 'sound']:
                        param_value = f'"{param_value}"'
                    params.append(param_value)
            
            block_code = self.convert_to_c(block.block_type, block.block_info['code'], params)
            indented_code = "    " * indent + block_code
            
            for line in indented_code.split('\n'):
                code.append(line)
            
            for connected_block in block.connected_blocks:
                traverse_block(connected_block, indent + 1)
        
        for block in self.elements:
            if not any(block in other.connected_blocks for other in self.elements):
                traverse_block(block)
        
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
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[('C Source File', '*.c')]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(c_program))
            messagebox.showinfo("Success", "C code exported successfully!")
    
    def convert_to_c(self, block_type, block_code, params):
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
        
        for block in self.elements:
            if not block.connected_blocks and not any(block in other.connected_blocks for other in self.elements):
                errors.append(f"Block '{block.block_type}' is not connected to any other block")
        
        for block in self.elements:
            if block.block_info.get('params'):
                for param in block.block_info['params']:
                    param_value = getattr(block, f"param_{param}").get()
                    if not param_value:
                        errors.append(f"Block '{block.block_type}' is missing required parameter '{param}'")
        
        return errors
    
    def run_project(self):
        errors = self.validate_blocks()
        if errors:
            error_message = "Cannot run project due to the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Run Error", error_message)
            return
        
        code = self.export_to_code()
        try:
            execution_window = ctk.CTkToplevel(self.master)
            execution_window.title("Project Execution")
            execution_window.geometry("400x300")
            
            output_area = ctk.CTkTextbox(execution_window)
            output_area.pack(fill="both", expand=True, padx=10, pady=10)
            
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
        
        GRID_SIZE = 20
        SNAP_DISTANCE = 30
        
        closest_block = None
        min_distance = float('inf')
        
        for block in self.elements:
            if block != dragged_block:
                block_coords = (block.winfo_x(), block.winfo_y())
                block_top = block_coords[1]
                block_center_x = block_coords[0] + (block.winfo_width() / 2)
                
                vertical_distance = abs(dragged_bottom - block_top)
                horizontal_distance = abs(dragged_center_x - block_center_x)
                
                if (vertical_distance < SNAP_DISTANCE and 
                    horizontal_distance < SNAP_DISTANCE and 
                    vertical_distance < min_distance):
                    min_distance = vertical_distance
                    closest_block = block
        
        if closest_block:
            block_coords = (closest_block.winfo_x(), closest_block.winfo_y())
            
            dragged_block.place(
                x=block_coords[0],
                y=block_coords[1] - dragged_block.winfo_height()
            )
            
            if closest_block not in dragged_block.connected_blocks:
                for block in self.elements:
                    if dragged_block in block.connected_blocks:
                        block.connected_blocks.remove(dragged_block)
                dragged_block.connected_blocks.clear()
                
                dragged_block.connected_blocks.append(closest_block)
                closest_block.connected_blocks.append(dragged_block)
                
                dragged_block.configure(border_color="#00ff00")
                closest_block.configure(border_color="#00ff00")
                
                self.draw_connection_line(closest_block, dragged_block)

    def draw_connection_line(self, block1, block2):
        for tag in self.canvas.find_withtag("connection"):
            self.canvas.delete(tag)
        
        coords1 = (block1.winfo_x(), block1.winfo_y())
        coords2 = (block2.winfo_x(), block2.winfo_y())
        
        x1 = coords1[0] + block1.winfo_width() / 2
        y1 = coords1[1] + block1.winfo_height()
        x2 = coords2[0] + block2.winfo_width() / 2
        y2 = coords2[1]
        
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
                
                if 'theme' in settings:
                    ctk.set_appearance_mode(settings['theme'])
                
                self.SNAP_DISTANCE = int(settings.get('snap_distance', 30))
                
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")

    def open_text_editor(self):
        editor = TextIde(game_engine=self)
        editor.run()

    def open_bitmap_editor(self):
        bitmap_editor = PaintEngine(self.master)
        bitmap_editor.run()
        
        if os.path.exists("bitmap.h"):
            with open("bitmap.h", "r") as f:
                bitmap_content = f.read()
            
            bitmap_name = simpledialog.askstring("Bitmap Name", "Enter a name for this bitmap:")
            if bitmap_name:
                if not os.path.exists("bitmaps"):
                    os.makedirs("bitmaps")
                
                with open(f"bitmaps/{bitmap_name}.h", "w") as f:
                    f.write(bitmap_content)
                
                self.block_categories['Graphics']['bitmap'] = {
                    'code': f'display_bitmap("{bitmap_name}")',
                    'params': ['bitmap_name'],
                    'color': '#FF5252',
                    'border_color': '#CC4040'
                }
                
                self.create_block_categories()
                messagebox.showinfo("Success", f"Bitmap '{bitmap_name}' has been added to the Graphics category!")
                
                # Clean up temporary bitmap file
                try:
                    os.remove("bitmap.h")
                except:
                    pass

    def delete_selected_block(self, event=None):
        if self.selected_block:
            self.selected_block.delete_block()
            self.selected_block = None
    
    def redraw_connections(self):
        for tag in self.canvas.find_withtag("connection"):
            self.canvas.delete(tag)
        
        for block in self.elements:
            for connected_block in block.connected_blocks:
                if self.elements.index(connected_block) > self.elements.index(block):
                    self.draw_connection_line(block, connected_block)

    def deselect_all_blocks(self, event):
        if event.widget == self.canvas:
            for block in self.elements:
                block.deselect_block()
            self.selected_block = None

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("ForgeeEngine")
        self.root.geometry("1024x768")

        self.recent_projects_list = self.load_recent_projects()
        
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        self.menu_frame = ctk.CTkFrame(
            self.main_container,
            corner_radius=20,
            fg_color=("#f0f0f0", "#2b2b2b"),
            border_width=2,
            border_color=("#e0e0e0", "#404040")
        )
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.7)
        
        self.title_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=20, pady=(30, 20))

        self.label = ctk.CTkLabel(
            self.title_frame,
            text="ForgeeEngine",
            font=("Arial", 32, "bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        self.label.pack()
        
        self.subtitle = ctk.CTkLabel(
            self.title_frame,
            text="A Game Engines",
            font=("Arial", 14),
            text_color=("#666666", "#aaaaaa")
        )
        self.subtitle.pack(pady=(0, 20))

        self.buttons_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=40, pady=20)
        
        self.create_project_button = ctk.CTkButton(
            self.buttons_frame,
            text="Create New Project",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.create_project
        )
        self.create_project_button.pack(fill="x", pady=(0, 10))

        self.open_project_button = ctk.CTkButton(
            self.buttons_frame,
            text="Open Project",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.open_project
        )
        self.open_project_button.pack(fill="x", pady=(0, 10))
        
        self.settings_button = ctk.CTkButton(
            self.buttons_frame,
            text="Settings",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.settings
        )
        self.settings_button.pack(fill="x", pady=(0, 10))

        self.quit_button = ctk.CTkButton(
            self.buttons_frame,
            text="Quit",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=self.quit
        )
        self.quit_button.pack(fill="x", pady=(0, 10))
        
        self.recent_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.recent_frame.pack(fill="x", padx=40, pady=20)

        self.recent_projects_label = ctk.CTkLabel(
            self.recent_frame,
            text="Recent Projects",
            font=("Arial", 14, "bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        self.recent_projects_label.pack(anchor="w", pady=(0, 10))

        self.recent_projects_combobox = ctk.CTkComboBox(
            self.recent_frame,
            values=self.recent_projects_list,
            font=("Arial", 12),
            height=35,
            corner_radius=8,
            border_color=("#e0e0e0", "#404040"),
            button_color="#40BF4A",
            button_hover_color="#2E8A35",
            command=self.open_recent_project
        )
        self.recent_projects_combobox.pack(fill="x")

    def load_recent_projects(self):
        try:
            if os.path.exists('recent_projects.json'):
                with open('recent_projects.json', 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def save_recent_projects(self):
        try:
            with open('recent_projects.json', 'w') as f:
                json.dump(self.recent_projects_list, f)
        except Exception:
            pass

    def add_recent_project(self, project_path):
        if project_path in self.recent_projects_list:
            self.recent_projects_list.remove(project_path)
        self.recent_projects_list.insert(0, project_path)
        self.recent_projects_list = self.recent_projects_list[:5]
        self.recent_projects_combobox.configure(values=self.recent_projects_list)
        self.save_recent_projects()

    def quit(self):
        self.root.destroy()

    def open_project(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Forgee Engine Project", "*.fge")]
        )
        if file_path:
            game_engine_window = ctk.CTkToplevel(self.root)
            game_engine = GameEngine(game_engine_window)
            game_engine.load_project(file_path)
            game_engine_window.mainloop()

    def create_project(self):
        create_window = ctk.CTkToplevel(self.root)
        create_window.title("Create New Project")
        create_window.geometry("400x300")

        create_frame = ctk.CTkFrame(
            create_window,
            corner_radius=15,
            fg_color=("#f0f0f0", "#2b2b2b"),
            border_width=2,
            border_color=("#e0e0e0", "#404040")
        )
        create_frame.pack(fill="both", expand=True, padx=20, pady=20)

        project_name_label = ctk.CTkLabel(
            create_frame,
            text="Project Name",
            font=("Arial", 16, "bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        project_name_label.pack(pady=(30, 10))

        project_name_entry = ctk.CTkEntry(
            create_frame,
            width=250,
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            placeholder_text="Enter project name..."
        )
        project_name_entry.pack(pady=10)

        create_button = ctk.CTkButton(
            create_frame,
            text="Create Project",
            font=("Arial", 14, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=lambda: self.create_project_file(project_name_entry.get())
        )
        create_button.pack(pady=20)

    def create_project_file(self, project_name):
        if not project_name:
            messagebox.showerror("Error", "Please enter a project name")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".fge",
            filetypes=[("Game Engine Projects", "*.fge")],
            initialfile=project_name
        )
        
        if file_path:
            self.add_recent_project(file_path)
            game_engine_window = ctk.CTkToplevel(self.root)
            game_engine = GameEngine(game_engine_window)

    def open_recent_project(self, project_name):
        if project_name:
            game_engine_window = ctk.CTkToplevel(self.root)
            game_engine = GameEngine(game_engine_window, project_name)

    def settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")

        settings_frame = ctk.CTkFrame(
            settings_window,
            corner_radius=15,
            fg_color=("#f0f0f0", "#2b2b2b"),
            border_width=2,
            border_color=("#e0e0e0", "#404040")
        )
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        settings_label = ctk.CTkLabel(
            settings_frame,
            text="Settings",
            font=("Arial", 20, "bold"),
            text_color=("#2b2b2b", "#ffffff")
        )
        settings_label.pack(pady=(20, 30))
        
        theme_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=30, pady=10)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=("Arial", 14),
            text_color=("#2b2b2b", "#ffffff")
        )
        theme_label.pack(side="left", padx=(0, 10))
        
        theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=["System", "Dark", "Light"],
            font=("Arial", 12),
            height=35,
            corner_radius=8,
            command=self.change_theme
        )
        theme_combo.pack(side="left", fill="x", expand=True)
        theme_combo.set(ctk.get_appearance_mode())

        save_button = ctk.CTkButton(
            settings_frame,
            text="Save Settings",
            font=("Arial", 14, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#40BF4A",
            hover_color="#2E8A35",
            command=lambda: self.save_settings(theme_combo.get())
        )
        save_button.pack(pady=30)

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def save_settings(self, theme):
        settings = {
            'theme': theme
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()