import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PaintEngine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Черно-белый экран")
        self.root.geometry("800x640")

        self.canvas = tk.Canvas(self.root, width=512, height=256, bg="white")
        self.canvas.pack()

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

        self.brush_slider = tk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, label="Brush size")
        self.brush_slider.pack()
        self.eraser_slider = tk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, label="Eraser size")
        self.eraser_slider.pack()

        self.brush_slider.bind("<B1-Motion>", self.update_brush_size)
        self.eraser_slider.bind("<B1-Motion>", self.update_eraser_size)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<B3-Motion>", self.erase)

        self.save_button = tk.Button(self.root, text="Save bitmap", command=self.save_bitmap_h)
        self.save_button.pack()

        self.open_button = tk.Button(self.root, text="Open image", command=self.open_image)
        self.open_button.pack()

        self.image = None

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

    def update_brush_size(self, event):
        self.brush_size = self.brush_slider.get()

    def update_eraser_size(self, event):
        self.eraser_size = self.eraser_slider.get()

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

if __name__ == "__main__":
    paint_engine = PaintEngine()
    paint_engine.run()