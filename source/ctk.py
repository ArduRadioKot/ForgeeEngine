import customtkinter as ctk

class SimpleEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.text = ctk.CTkTextbox(self, width=600, height=400)
        self.text.pack(side=ctk.RIGHT, fill="both", expand=True)
        self.text.bind("<KeyRelease>", self.auto_brace)
        self.line_number_area = ctk.CTkTextbox(self, width=50, height=400)
        self.line_number_area.pack(side=ctk.LEFT, fill="y")
        self.update_line_numbers()

    def auto_brace(self, event):
        if event.char in "{}[]()<>":
            self.text.insert("insert", event.char)
            self.text.insert("insert", self.get_closing_brace(event.char))
            self.text.mark_set("insert", "insert + 1")

    def get_closing_brace(self, char):
        braces = {"{": "}", "[": "]", "(": ")", "<":">"}
        return braces[char]

    def update_line_numbers(self):
        self.line_number_area.delete("1.0", "end")
        for i, line in enumerate(self.text.get("1.0", "end").split("\n"), start=1):
            self.line_number_area.insert("end", f"{i}\n")
        self.after(100, self.update_line_numbers)

if __name__ == "__main__":
    app = SimpleEditor()
    app.mainloop()