import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json

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
        text_frame = ctk.CTkFrame(self.main_frame)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create line number area
        self.line_number_area = tk.Text(
            text_frame,
            width=4,
            padx=3,
            pady=5,
            font=("Consolas", 12),
            bg="#2b2b2b",
            fg="#808080",
            highlightthickness=0,
            borderwidth=0
        )
        self.line_number_area.pack(side="left", fill="y")
        
        # Create main text area
        self.text_area = tk.Text(
            text_frame,
            font=("Consolas", 12),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#d4d4d4",
            selectbackground="#264f78",
            selectforeground="#d4d4d4",
            highlightthickness=0,
            borderwidth=0,
            padx=5,
            pady=5
        )
        self.text_area.pack(side="left", fill="both", expand=True)

    def configure_syntax_highlighting(self):
        # Configure syntax highlighting tags
        self.text_area.tag_config('keyword', foreground='#569cd6')  # Blue
        self.text_area.tag_config('builtin', foreground='#4ec9b0')  # Teal
        self.text_area.tag_config('string', foreground='#ce9178')  # Orange
        self.text_area.tag_config('comment', foreground='#6a9955')  # Green
        self.text_area.tag_config('class', foreground='#4ec9b0')  # Teal
        self.text_area.tag_config('def_func', foreground='#dcdcaa')  # Yellow
        self.text_area.tag_config('number', foreground='#b5cea8')  # Light green
        self.text_area.tag_config('operator', foreground='#d4d4d4')  # White
        
        # Define syntax elements
        self.keywords = [
            'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally',
            'def', 'class', 'return', 'break', 'continue', 'pass', 'raise',
            'import', 'from', 'as', 'global', 'nonlocal', 'lambda', 'with',
            'yield', 'async', 'await', 'in', 'is', 'not', 'and', 'or'
        ]
        
        self.builtins = [
            'print', 'len', 'range', 'list', 'dict', 'set', 'int', 'float',
            'str', 'bool', 'True', 'False', 'None', 'self', 'super', 'open',
            'close', 'read', 'write', 'append', 'extend', 'pop', 'remove',
            'sort', 'reverse', 'split', 'join', 'strip', 'replace', 'find'
        ]
        
        self.operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=']

    def update_line_numbers(self):
        self.line_number_area.delete("1.0", "end")
        for i, line in enumerate(self.text_area.get("1.0", "end").split("\n"), start=1):
            self.line_number_area.insert("end", f"{i}\n")
        self.after(100, self.update_line_numbers)

    def highlight_syntax_realtime(self, event=None):
        # Remove all existing tags
        for tag in ['keyword', 'builtin', 'string', 'comment', 'class', 'def_func', 'number', 'operator']:
            self.text_area.tag_remove(tag, '1.0', 'end')
        
        text = self.text_area.get('1.0', 'end-1c')
        lines = text.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Highlight comments
            if '#' in line:
                comment_start = line.index('#')
                self.text_area.tag_add('comment', f'{i}.{comment_start}', f'{i}.end')
            
            # Split line into words while preserving operators
            words = []
            current_word = ''
            for char in line:
                if char in ' \t()[]{},.;:+-*/=<>!':
                    if current_word:
                        words.append(current_word)
                        current_word = ''
                    if char not in ' \t':
                        words.append(char)
                else:
                    current_word += char
            if current_word:
                words.append(current_word)
            
            # Highlight words
            for word in words:
                if word in self.keywords:
                    self.highlight_word(word, i, 'keyword')
                elif word in self.builtins:
                    self.highlight_word(word, i, 'builtin')
                elif word in self.operators:
                    self.highlight_word(word, i, 'operator')
                elif word.isdigit():
                    self.highlight_word(word, i, 'number')
                elif word.startswith('"') or word.startswith("'"):
                    self.highlight_word(word, i, 'string')
                elif word == 'def':
                    self.highlight_word(word, i, 'def_func')
                elif word == 'class':
                    self.highlight_word(word, i, 'class')

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
        # Update text area colors based on theme
        if theme == "Dark":
            self.text_area.configure(bg="#1e1e1e", fg="#d4d4d4")
            self.line_number_area.configure(bg="#2b2b2b", fg="#808080")
        else:
            self.text_area.configure(bg="#ffffff", fg="#000000")
            self.line_number_area.configure(bg="#f0f0f0", fg="#808080")

    def change_font_size(self, size):
        font = ("Consolas", int(size))
        self.text_area.configure(font=font)
        self.line_number_area.configure(font=font)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = TextIde()
    app.run()