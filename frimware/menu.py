import tkinter as tk
from tkinter import filedialog, messagebox
import game_engine as ge 
from game_engine import GameEngine 
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("ForgeeEngine")
        self.root.geometry("800x600")

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.menu_frame, text="ForgeeEngine", font=("Arial", 24))
        self.label.pack(pady=20)

        self.open_project_button = tk.Button(self.menu_frame, text="Открыть проект", command=self.open_project)
        self.open_project_button.pack(pady=10)

        self.create_project_button = tk.Button(self.menu_frame, text="Создать проект", command=self.create_project)
        self.create_project_button.pack(pady=10)

        self.settings_button = tk.Button(self.menu_frame, text="Настройки", command=self.settings)
        self.settings_button.pack(pady=10)

        self.quit_button = tk.Button(self.menu_frame, text="Выйти", command=self.quit)
        self.quit_button.pack(pady=10)

        self.recent_projects_label = tk.Label(self.menu_frame, text="Недавно созданные проекты:")
        self.recent_projects_label.pack(pady=10)

        self.recent_projects_listbox = tk.Listbox(self.menu_frame, width=40, height=10)
        self.recent_projects_listbox.pack(pady=10)
        self.recent_projects_listbox.bind("<<ListboxSelect>>", self.open_recent_project)
        self.recent_projects_list = []


    def quit(self):
        self.root.destroy()


    def open_project(self):
        # Открыть файловый диалог для выбора проекта
        file_path = filedialog.askopenfilename(title="Выберите проект", filetypes=[("Game Engine Projects", "*.fge")])
        if file_path:
            # Открыть проект в новом окне
            game_engine_window = tk.Toplevel(self.root)
            game_engine = GameEngine(game_engine_window, file_path)

    def create_project(self):
        # Создать новый проект в новом окне
        create_window = tk.Toplevel(self.root)
        create_window.title("Создать проект")

        create_frame = tk.Frame(create_window)
        create_frame.pack(fill="both", expand=True)

        project_name_label = tk.Label(create_frame, text="Название проекта:")
        project_name_label.pack(pady=10)

        project_name_entry = tk.Entry(create_frame, width=20)
        project_name_entry.pack(pady=10)

        create_button = tk.Button(create_frame, text="Создать проект", command=lambda: self.create_project_file(project_name_entry.get()))
        create_button.pack(pady=10)

    def create_project_file(self, project_name):
        # Создать файл для проекта
        file_path = f"{project_name}.fge"
        with open(file_path, "w") as file:
            file.write("")

        # Добавить проект в список недавно созданных проектов
        self.recent_projects_list.append(file_path)
        self.recent_projects_listbox.insert(tk.END, project_name)

        # Открыть проект в новом окне
        game_engine_window = tk.Toplevel(self.root)
        game_engine = GameEngine(game_engine_window, file_path)

    # ... (rest of the code remains the same)
    def settings(self):
        # Создать окно настроек
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")

        settings_frame = tk.Frame(settings_window)
        settings_frame.pack(fill="both", expand=True)

        setting_label = tk.Label(settings_frame, text="Настройка:")
        setting_label.pack(pady=10)

        setting_entry = tk.Entry(settings_frame, width=20)
        setting_entry.pack(pady=10)

        save_button = tk.Button(settings_frame, text="Сохранить настройки", command=lambda: self.save_settings(setting_entry.get()))
        save_button.pack(pady=10)

    def save_settings(self, setting):
        # Сохранить настройку
        print(f"Настройка сохранена: {setting}")

    def open_recent_project(self, event):
        # Открыть проект из списка недавно созданных проектов
        selected_index = self.recent_projects_listbox.curselection()[0]
        file_path = self.recent_projects_list[selected_index]
        game_engine = ge.GameEngine(self.root, file_path)



root = tk.Tk()
main_app = MainMenu(root)
root.mainloop()