import customtkinter as ctk
from tkinter import filedialog, messagebox
import game_engine as ge 
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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
            game_engine_window = ctk.CTk()
            game_engine = ge.GameEngine(game_engine_window)
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
            game_engine = ge.GameEngine(game_engine_window)

    def open_recent_project(self, project_name):
        if project_name:
            game_engine_window = ctk.CTkToplevel(self.root)
            game_engine = ge.GameEngine(game_engine_window, project_name)

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
    main_app = MainMenu(root)
    root.mainloop()