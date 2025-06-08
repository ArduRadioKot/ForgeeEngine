import customtkinter as ctk
from tkinter import filedialog, messagebox
import game_engine as ge 
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
            game_engine = ge.GameEngine(game_engine_window, file_path)

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
        game_engine = ge.GameEngine(game_engine_window)  # Create GameEngine window without file path

    def open_recent_project(self, project_name):
        game_engine_window = ctk.CTkToplevel(self.root)
        game_engine = ge.GameEngine(game_engine_window, project_name)

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

root = ctk.CTk()
main_app = MainMenu(root) 
root.mainloop()