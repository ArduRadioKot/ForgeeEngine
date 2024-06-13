import tkinter as tk
from tkinter import filedialog, messagebox

class FileManager:
    def __init__(self, master):
        self.master = master
        self.master.title("File Manager")

        self.file_list = tk.Listbox(self.master)
        self.file_list.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.open_button = tk.Button(self.button_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.RIGHT)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as f:
                self.file_list.delete(0, tk.END)
                for line in f:
                    self.file_list.insert(tk.END, line.strip())

    def save_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as f:
                for i in range(self.file_list.size()):
                    f.write(self.file_list.get(i) + "\n")

root = tk.Tk()
file_manager = FileManager(root)
root.mainloop()