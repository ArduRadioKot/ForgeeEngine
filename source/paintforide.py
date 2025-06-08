import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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
        self.buttons_frame.pack(fill="x", pady=(0, 10))
        
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

if __name__ == "__main__":
    paint_engine = PaintEngine(None)
    paint_engine.run()