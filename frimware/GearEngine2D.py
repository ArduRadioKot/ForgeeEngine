from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, askopenfile, askdirectory
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial
import kivy.metrics
import os
from os import makedirs # this import for create folders
from os.path import exists # checking for folder existence
import webbrowser
#import plyer # notification in Win10
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


import numpy as np
import pyautogui
import time


WindowWidth = 1280
WindowHeight = 720


Window.clearcolor = (.2, .2, .2, 1)
Window.size = (WindowWidth, WindowHeight)

class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        


        self.label = Label(text = "GearEngine2D | (C) Stas Povalaev | Business | v.0.0.3a", color=(.5,.5,.5, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.03})
        self.add_widget(self.label)
        # Toolbar
        NewPrjBtn = Button(text = "New", size_hint = (.05, .05), pos_hint = {'center_x': 0.025, 'center_y': 0.97})
        NewPrjBtn.bind(on_press=self.create_project)
        self.add_widget(NewPrjBtn)
        RunPrjBtn = Button(text = "Run", size_hint = (.05, .05), pos_hint = {'center_x': 0.075, 'center_y': 0.97})
        RunPrjBtn.bind(on_press=self.run_project)
        self.add_widget(RunPrjBtn)
        ShowInfoBtn = Button(text = "Info", size_hint = (.05, .05), pos_hint = {'center_x': 0.125, 'center_y': 0.97})
        ShowInfoBtn.bind(on_press=self.open_popup_info)
        self.add_widget(ShowInfoBtn)
        OpenHelpBtn = Button(text = "Help", size_hint = (.05, .05), pos_hint = {'center_x': 0.175, 'center_y': 0.97})
        OpenHelpBtn.bind(on_press=self.open_help)
        self.add_widget(OpenHelpBtn)
        UpdateEngineBtn = Button(text = "Update Engine", size_hint = (.08, .05), pos_hint = {'center_x': 0.240, 'center_y': 0.97})
        UpdateEngineBtn.bind(on_press=self.update_engine)
        self.add_widget(UpdateEngineBtn)
        ReleaseNotesBtn = Button(text = "Release Notes", size_hint = (.08, .05), pos_hint = {'center_x': 0.320, 'center_y': 0.97})
        ReleaseNotesBtn.bind(on_press=self.release_notes)
        self.add_widget(ReleaseNotesBtn)
        AuthorsBtn = Button(text='Author',size_hint=(.05, .05),pos_hint = {'center_x': 0.385, 'center_y': 0.97})
        AuthorsBtn.bind(on_press=self.changer)
        self.add_widget(AuthorsBtn)
        SettingsBtn = Button(text='Settings',size_hint=(.05, .05),pos_hint = {'center_x': 0.435, 'center_y': 0.97})
        SettingsBtn.bind(on_press=self.changerSettings)
        self.add_widget(SettingsBtn)
        MainMenuBtn = Button(text='Main Menu',size_hint=(.07, .05),pos_hint = {'center_x': 0.495, 'center_y': 0.97})
        MainMenuBtn.bind(on_press=self.changerMainMenu)
        self.add_widget(MainMenuBtn)

        # ToolBal LEFT
        left_bar = GridLayout(cols=1, padding=2, spacing=2, size_hint=(.2, .93))
        left_bar.bind(minimum_height=left_bar.setter('height'))

        AddLabelBtn = Button(text = "Add Label", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.92})
        AddLabelBtn.bind(on_press=self.add_label)
        left_bar.add_widget(AddLabelBtn)
        AddButtonBtn = Button(text = "Add Button", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.87})
        AddButtonBtn.bind(on_press=self.add_button)
        left_bar.add_widget(AddButtonBtn)
        AddSoundBtn = Button(text = "Add Sound", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.82})
        AddSoundBtn.bind(on_press=self.add_sound)
        left_bar.add_widget(AddSoundBtn)
        AddFunctionBtn = Button(text = "Add Function", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.77})
        AddFunctionBtn.bind(on_press=self.add_function)
        left_bar.add_widget(AddFunctionBtn)
        AddCycleBtn = Button(text = "Add Cycle (While)", font_size='14sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.72})
        left_bar.add_widget(AddCycleBtn)

        AddTextureTypeBtn = Button(text = "Add Texture Type", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.67})
        AddTextureTypeBtn.bind(on_press=self.add_texture_type)
        left_bar.add_widget(AddTextureTypeBtn)

        AddTextureObjBtn = Button(text = "Add Texture Obj", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.62})
        AddTextureObjBtn.bind(on_press=self.add_texture_OBJ)
        left_bar.add_widget(AddTextureObjBtn)
        AddTextInputBtn = Button(text = "Add TextInput", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.57})
        AddTextInputBtn.bind(on_press=self.add_textinput)
        left_bar.add_widget(AddTextInputBtn)
        Button8 = Button(text = "Add Variable", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.52})
        left_bar.add_widget(Button8)
        AddLogicBtn = Button(text = "Add Logic", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.47})
        AddLogicBtn.bind(on_press=self.add_logic)
        left_bar.add_widget(AddLogicBtn)
        Button10 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.42})
        left_bar.add_widget(Button10)
        Button11 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.37})
        left_bar.add_widget(Button11)
        Button12 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.32})
        left_bar.add_widget(Button12)
        Button13 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.27})
        left_bar.add_widget(Button13)
        Button14 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.22})
        left_bar.add_widget(Button14)
        Button15 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.17})
        left_bar.add_widget(Button15)
        Button16 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.12})
        left_bar.add_widget(Button16)
        Button17 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.07})
        left_bar.add_widget(Button17)
        Button18 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button18)
        Button19 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button19)
        Button20 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button20)
        Button21 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button21)
        Button22 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button22)
        Button23 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button23)
        Button24 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button24)
        Button25 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button25)
        Button26 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button26)
        Button27 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button27)
        Button28 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button28)
        Button29 = Button(text = "", font_size='15sp', size_hint = (.1, .05), pos_hint = {'center_x': 0.050, 'center_y': 0.02})
        left_bar.add_widget(Button29)
        # 1_window.png
        bgImg1 = Image(source='man1.png', pos=(0,0), color=(.1,.1,.1, 0.5))
        self.add_widget(bgImg1)

        root = ScrollView(size=(.2, .93), pos_hint={'center_x': .5, 'center_y': .4}, do_scroll_x=False)
        root.add_widget(left_bar)

        self.add_widget(root)

        

        
 
       


        # ToolBar RIGHT
        AddLevelBtn = Button(text = "Add Level", size_hint = (.1, .05), pos_hint = {'center_x': 0.95, 'center_y': 0.92})
        AddLevelBtn.bind(on_press=self.add_level)
        self.add_widget(AddLevelBtn)
        self.TextDEFS = Label(text = "Functions:\n", color=(.9,.9,.9, 1), markup=True, font_size='15sp', size_hint = (.1, .9), pos_hint = {'center_x': 0.93, 'center_y': 0.86})
        self.add_widget(self.TextDEFS)


    def changer(self,*args):

        self.manager.current = 'screen2'


    def add_logic(self, instance):
        #bgImg1 = Image(source='man1.png', pos=(0,0), color=(.1,.1,.1, 0.5))
        layout = BoxLayout(orientation="vertical")
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        textinput_posX = TextInput(text='pos X (in pixels)', background_normal='man3.png', font_size='12sp')
        textinput_posY = TextInput(text='pos Y (in pixels)', background_normal='man3.png', font_size='12sp')
        object_settings_lbl = Label(text="Object type: Logic", font_size='12sp')
        object_name_lbl = Label(text="object name:", font_size='12sp')
        object_pos_lbl = Label(text="position:", font_size='12sp')
        object_color_lbl = Label(text="color: \n Example - (.1,.1,.1, 1)", font_size='12sp')
        object_source_lbl = Label(text="source .png file:", font_size='12sp')
        textinput_class_name = TextInput(text='TypeName', background_normal='man3.png', font_size='12sp')
        textinput_source = TextInput(text='C/to/file', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_pos_lbl)
        layout.add_widget(textinput_posX)
        layout.add_widget(textinput_posY)
        layout.add_widget(object_color_lbl)
        layout.add_widget(textinput_class_name)
        layout.add_widget(object_source_lbl)
        layout.add_widget(textinput_source)
        layout.add_widget(button)
        
        popup = Popup(title='New Texture Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_texture_OBJ, textinput_name, textinput_source, textinput_posX, textinput_posY, textinput_class_name))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_add_logic(self, textinput_name, textinput_source, textinput_posX, textinput_posY, textinput_class_name, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Logic")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# OBJECT DEFINITIONS', '\n'+textinput_name.text+' = '+textinput_class_name.text+'(source="'+textinput_source.text+'", pos=('+textinput_posX.text+','+textinput_posY.text+'))\n# OBJECT DEFINITIONS'))
        
        with open(FILE_NAME, 'rt', encoding='utf-8') as src1:
            data1 = src1.read()
        
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest1:
            dest1.write(data1.replace('# ADD OBJECTS', 'm.add_widget('+textinput_name.text+')\n        # ADD OBJECTS'))


    def open_popup_info(self, instance):
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Ehhhhhehey broo is a one-man engine.\n I hope you enjoy using it. Click on the Help\n button. There is a lot of useful information\n in the documentation!\n Forgive me if there are any shortcomings in the \nprogram. I work alone. I was born on\n July 16, 2006. I'm not sure I can think of everything.\n Author YouTube: Ixieane | Contact: lazarusgames1@gmail.com\n *GearEngine2D | Python 3.10 | 2021-2022 | x64-bit*", font_size='12sp'))
        button = Button(text='Close')
        layout.add_widget(button)
        popup = Popup(title='GearEngine2D', content=layout, size_hint=(None, None), size=(500, 500))
        button.bind(on_press=popup.dismiss)
        popup.open()


    



    def changerSettings(self,*args):

        self.manager.current = 'screen3'

    def changerMainMenu(self,*args):

        self.manager.current = 'screen0'

    def test(self,instance):
        print('This is a test')

    def create_project(self, instance):
        layout = BoxLayout(orientation="vertical")
        label_project_info = Label(text="Creating project", font_size='12sp')
        project_name = Label(text="project name:", font_size='12sp')
        project_textinput_name = TextInput(text='project', background_normal='man3.png', font_size='12sp')
        project_window_width_label = Label(text="window width:", font_size='12sp')
        project_window_width = TextInput(text='500', background_normal='man3.png', font_size='12sp')
        project_window_height_label = Label(text="window height:", font_size='12sp')
        project_window_height = TextInput(text='500', background_normal='man3.png', font_size='12sp')
        project_window_color_label = Label(text="window color:", font_size='12sp')
        project_window_color_textinput = TextInput(text='(.4, .8, .4, 1)', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(label_project_info)
        layout.add_widget(project_name)
        layout.add_widget(project_textinput_name)
        layout.add_widget(project_window_width_label)
        layout.add_widget(project_window_width)
        layout.add_widget(project_window_height_label)
        layout.add_widget(project_window_height)
        layout.add_widget(project_window_color_label)
        layout.add_widget(project_window_color_textinput)
        layout.add_widget(button)
        popup = Popup(title='New Label Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_project, project_window_width, project_textinput_name, project_window_height, project_window_color_textinput))
        # СОЗДАНИЕ ОКНА РЕДАКТОРА
        
        button.bind(on_press=popup.dismiss)

        popup.open()

         

    def write_file_project(self, project_window_width, project_textinput_name, project_window_height, project_window_color_textinput, *args):
        fld = ('projects\\' + project_textinput_name.text) # needed path
        if not exists(fld):# if this directory does not exist
            makedirs(fld) # create a directory


        with open(f'{fld}\\level_1.py', 'w') as NewPrj_main: # Create "main.py" in X/Y directory
            NewPrj_main.write(" \n")
            NewPrj_main.write("# IMPORTS\n")
            NewPrj_main.write("from kivy.app import App\n")
            NewPrj_main.write("from kivy.uix.widget import Widget\n")
            NewPrj_main.write("from kivy.uix.image import Image\n")
            NewPrj_main.write("from kivy.core.window import Window\n")
            NewPrj_main.write("from kivy.uix.label import Label\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("# VARIABLES\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("WindowWidth = "+project_window_width.text+"\n")
            NewPrj_main.write("WindowHeight = "+project_window_height.text+"\n")
            NewPrj_main.write("Window.clearcolor = "+project_window_color_textinput.text+"\n")
            NewPrj_main.write("Window.size = (WindowWidth, WindowHeight)\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("class character(Widget):\n")
            NewPrj_main.write("    pass\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("m = character()\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("# CLASSES\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("# OBJECT DEFINITIONS\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("class gameApp(App):\n")
            NewPrj_main.write("    def build(self):\n")
            NewPrj_main.write("        self.title = '"+project_textinput_name.text+"'\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("        #m.add_widget(labelLOG)\n")
            NewPrj_main.write("        # ADD OBJECTS\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("        return m\n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write(" \n")
            NewPrj_main.write("if __name__ == '__main__':\n")
            NewPrj_main.write("    gameApp().run()\n")
            



            with open(f'{fld}\\'+project_textinput_name.text+".log", 'w') as NewPrj_kv:
                NewPrj_kv.write("# GearEngine2D project | LOG \n")
                EditorWindowPNG_width = str(int(project_window_width.text) % 2)
                EditorWindowPNG_height = str(int(project_window_height.text) % 2)
                print(EditorWindowPNG_width)
                EditorWindowPNG = Image(source='1_window.png', pos=(200, 100), size=(.4,.1), size_hint=(.4,.1), color=(1,1,1, 1))
                self.add_widget(EditorWindowPNG)
        
                #plyer.notification.notify(message='project successfully created', app_name='GearEngine2D', title='GearEngine2D')


    def add_texture_type(self, instance):
        #bgImg1 = Image(source='man1.png', pos=(0,0), color=(.1,.1,.1, 0.5))
        layout = BoxLayout(orientation="vertical")
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(textinput_name)
        layout.add_widget(button)
        
        popup = Popup(title='New Texture Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_texture, textinput_name))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_texture(self, textinput_name, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Texture")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# CLASSES', '\nclass '+textinput_name.text+'(Image):\n \n    def __init__(self, **kwargs):\n        super('+textinput_name.text+', self).__init__(**kwargs)\n        self._keyboard = Window.request_keyboard(None, self)\n        if not self._keyboard:\n            return\n        self._keyboard.bind(on_key_down=self.on_keyboard_down)\n \n    def on_keyboard_down(self, keyboard, keycode, text, modifiers):# COLLISION\n        if keycode[1] == "a":\n            self.x -= 10\n        elif keycode[1] == "d":\n            self.x += 10\n        elif keycode[1] == "w":\n            self.y += 10\n        elif keycode[1] == "s":\n            self.y -= 10\n        else:\n            return False\n        return True\n# CLASSES'))

    def add_texture_OBJ(self, instance):
        #bgImg1 = Image(source='man1.png', pos=(0,0), color=(.1,.1,.1, 0.5))
        layout = BoxLayout(orientation="vertical")
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        textinput_posX = TextInput(text='pos X (in pixels)', background_normal='man3.png', font_size='12sp')
        textinput_posY = TextInput(text='pos Y (in pixels)', background_normal='man3.png', font_size='12sp')
        object_settings_lbl = Label(text="Object type: Texture", font_size='12sp')
        object_name_lbl = Label(text="object name:", font_size='12sp')
        object_pos_lbl = Label(text="position:", font_size='12sp')
        object_color_lbl = Label(text="color: \n Example - (.1,.1,.1, 1)", font_size='12sp')
        object_source_lbl = Label(text="source .png file:", font_size='12sp')
        textinput_class_name = TextInput(text='TypeName', background_normal='man3.png', font_size='12sp')
        textinput_source = TextInput(text='C/to/file', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_pos_lbl)
        layout.add_widget(textinput_posX)
        layout.add_widget(textinput_posY)
        layout.add_widget(object_color_lbl)
        layout.add_widget(textinput_class_name)
        layout.add_widget(object_source_lbl)
        layout.add_widget(textinput_source)
        layout.add_widget(button)
        
        popup = Popup(title='New Texture Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_texture_OBJ, textinput_name, textinput_source, textinput_posX, textinput_posY, textinput_class_name))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_texture_OBJ(self, textinput_name, textinput_source, textinput_posX, textinput_posY, textinput_class_name, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Texture")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# OBJECT DEFINITIONS', '\n'+textinput_name.text+' = '+textinput_class_name.text+'(source="'+textinput_source.text+'", pos=('+textinput_posX.text+','+textinput_posY.text+'))\n# OBJECT DEFINITIONS'))
        
        with open(FILE_NAME, 'rt', encoding='utf-8') as src1:
            data1 = src1.read()
        
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest1:
            dest1.write(data1.replace('# ADD OBJECTS', 'm.add_widget('+textinput_name.text+')\n        # ADD OBJECTS'))



    def add_function(self, instance):
        #self.TextDEFS.text = self.TextDEFS.text + "\n Типа функция "
        # добавление функции
        #def1_name = input("function name: ")
        layout = BoxLayout(orientation="vertical")
        textinput_name_type = Label(text="Object type: Function", font_size='12sp')
        label_function_name = Label(text="object name:", font_size='12sp')
        textinput_name_def = TextInput(text='function_name', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(textinput_name_type)
        layout.add_widget(label_function_name)
        layout.add_widget(textinput_name_def)
        layout.add_widget(button)
        popup = Popup(title='New Function Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_function, textinput_name_def))
        button.bind(on_press=popup.dismiss)

        popup.open()

    def write_file_function(self, textinput_name_def, *args):

        global FILE_NAME
        inp = askopenfile(mode="r", title="add Function")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# DEFS', '# Function\n    def '+textinput_name_def.text+'(self, instance):\n        pass\n# DEFS\n'))


        self.TextDEFS.text = self.TextDEFS.text + textinput_name_def.text+"\n"

    def add_label(self, instance):
        # lines.insert(39, 'Text\n')
        #
        #
        #
        layout = BoxLayout(orientation="vertical")
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        textinput_posX = TextInput(text='pos X', background_normal='man3.png', font_size='12sp')
        textinput_posY = TextInput(text='pos Y', background_normal='man3.png', font_size='12sp')
        object_settings_lbl = Label(text="Object type: Label", font_size='12sp')
        object_name_lbl = Label(text="object name:", font_size='12sp')
        object_pos_lbl = Label(text="position:", font_size='12sp')
        object_size_lbl = Label(text="size:", font_size='12sp')
        object_text_lbl = Label(text="text:", font_size='12sp')
        textinput_width = TextInput(text='5', background_normal='man3.png', font_size='12sp')
        textinput_height = TextInput(text='5', background_normal='man3.png', font_size='12sp')
        textinput_text = TextInput(text='text', background_normal='man3.png', font_size='12sp')
        lbl_font_size = Label(text="font size:", font_size='12sp')
        textinput_font_size = TextInput(text='', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_pos_lbl)
        layout.add_widget(textinput_posX)
        layout.add_widget(textinput_posY)
        layout.add_widget(object_size_lbl)
        layout.add_widget(textinput_width)
        layout.add_widget(textinput_height)
        layout.add_widget(object_text_lbl)
        layout.add_widget(textinput_text)
        layout.add_widget(lbl_font_size)
        layout.add_widget(textinput_font_size)
        layout.add_widget(button)
        
        popup = Popup(title='New Label Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_label, textinput_name, textinput_text, textinput_font_size, textinput_width, textinput_height, textinput_posX, textinput_posY))
        # РЕДАКТОР

        
        popup.open()


        #EditorLabel_width = (int(textinput_width.text) / 3)
        #EditorLabel_height = (int(textinput_height.text) / 3)
        
        button.bind(on_press=popup.dismiss)
        ################################################

    def write_file_label(self, textinput_name, textinput_text, textinput_font_size, textinput_width, textinput_height, textinput_posX, textinput_posY, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Label")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# CODE', '# Label '+textinput_name.text+'\n        '+textinput_name.text+"=Label(text ="+"'"+textinput_text.text+"'"+", font_size='"+textinput_font_size.text+"sp', size_hint =("+textinput_width.text+","+textinput_height.text+"), pos_hint = {'center_x': "+textinput_posX.text+", 'center_y':"+textinput_posY.text+"})\n        main_layout.add_widget("+textinput_name.text+")\n# CODE\n"))
            EditorLabel = Label(text = textinput_text.text, color=(0,0,0, 1), size_hint =(.5, .5), pos_hint = {'center_x': 0.5, 'center_y': .5})
            self.add_widget(EditorLabel)
            

    
    def add_button(self, instance):
        # lines.insert(39, 'Text\n')
        # ôàéë  äîáàâ.  íîìåð ñòðîêè  òåêñò
        #
        #
        layout = BoxLayout(orientation="vertical")
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        textinput_posX = TextInput(text='pos X', background_normal='man3.png', font_size='12sp')
        textinput_posY = TextInput(text='pos Y', background_normal='man3.png', font_size='12sp')
        object_settings_lbl = Label(text="Object type: Button", font_size='12sp')
        object_name_lbl = Label(text="object name:", font_size='12sp')
        object_pos_lbl = Label(text="position:", font_size='12sp')
        object_size_lbl = Label(text="size:", font_size='12sp')
        object_text_lbl = Label(text="text:", font_size='12sp')
        textinput_width = TextInput(text='width', background_normal='man3.png', font_size='12sp')
        textinput_height = TextInput(text='height', background_normal='man3.png', font_size='12sp')
        textinput_text = TextInput(text='text', background_normal='man3.png', font_size='12sp')
        lbl_font_size = Label(text="font size:", font_size='12sp')
        textinput_font_size = TextInput(text='', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_pos_lbl)
        layout.add_widget(textinput_posX)
        layout.add_widget(textinput_posY)
        layout.add_widget(object_size_lbl)
        layout.add_widget(textinput_width)
        layout.add_widget(textinput_height)
        layout.add_widget(object_text_lbl)
        layout.add_widget(textinput_text)
        layout.add_widget(lbl_font_size)
        layout.add_widget(textinput_font_size)
        layout.add_widget(button)
        
        popup = Popup(title='New Button Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_button, textinput_name, textinput_text, textinput_font_size, textinput_width, textinput_height, textinput_posX, textinput_posY))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_button(self, textinput_name, textinput_text, textinput_font_size, textinput_width, textinput_height, textinput_posX, textinput_posY, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Label")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# CODE', '# Button '+textinput_name.text+'\n        '+textinput_name.text+"=Button(text ="+"'"+textinput_text.text+"'"+", font_size='"+textinput_font_size.text+"sp', size_hint =("+textinput_width.text+","+textinput_height.text+"), pos_hint = {'center_x': "+textinput_posX.text+", 'center_y':"+textinput_posY.text+"})\n        main_layout.add_widget("+textinput_name.text+")\n# CODE\n"))
            

    
    def run_project(self, instance):
        # lines.insert(39, 'Text\n')
        #
        #
        #
        global FILE_NAME
        inp = askopenfile(mode="r", title="Which file to run")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)
        current_file = FILE_NAME
        print("current_file: " + current_file)

        
        with open(FILE_NAME) as NewPrj_kv:
            os.system("python " + '"' + FILE_NAME + '"')


    def add_sound(self,instance):
        #messagebox.showinfo("Basic Example", "a Basic Tk MessageBox")
        #messagebox.showerror("Basic Example", "a Basic Tk MessageBox")
        #messagebox.showwarning("Basic Example", "a Basic Tk MessageBox")

        
        #from kivy.core import audio
        #sound = SoundLoader.load('mytest.wav')
        #sound.play()
        #plyer.notification.notify(message='This is not yet available in GearEngine2D', app_name='GearEngine2D', title='GearEngine2D')
        layout = BoxLayout(orientation="vertical")
        object_settings_lbl = Label(text="Object type: Sound", font_size='12sp')
        object_name_lbl = Label(text="Sound name:", font_size='12sp')
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        object_sound_source_lbl = Label(text="Sound source (.wav):", font_size='12sp')
        object_sound_source = TextInput(text='"C/path/to/file"', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_sound_source_lbl)
        layout.add_widget(object_sound_source)
        layout.add_widget(button)
        
        popup = Popup(title='New Sound Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_sound, textinput_name, object_sound_source))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_sound(self, textinput_name, object_sound_source, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add Sound")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# CODE', '# Sound '+textinput_name.text+'\n        '+textinput_name.text+' = SoundLoader.load('+object_sound_source.text+')\n        #'+textinput_name.text+'.play()\n# CODE'))

    def add_level(self, instance):
        layout = BoxLayout(orientation="vertical")
        object_settings_lbl = Label(text="Object type: Level", font_size='12sp')
        object_name_lbl = Label(text="Name level:", font_size='12sp')
        object_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        object_size_lbl = Label(text="Window Size:", font_size='12sp')
        object_width = TextInput(text='width in pixels', background_normal='man3.png', font_size='12sp')
        object_height = TextInput(text='height in pixels', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(object_name)
        layout.add_widget(object_size_lbl)
        layout.add_widget(object_width)
        layout.add_widget(object_height)
        layout.add_widget(button)
        
        popup = Popup(title='New Level Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_level, object_width, object_height, object_name))
        button.bind(on_press=popup.dismiss)
        popup.open()

        ################################################

    def write_file_level(self, object_width, object_height, object_name, *args):

        
       
        global FILE_NAME
        inp1 = askdirectory(title="Choose Folder")
        #inp = askopenfile(mode="r", title="add Level")
        #if inp is None:
            #return
        #FILE_NAME = inp.name
        #print(FILE_NAME)
        #print(inp)

        with open(f'{inp1}\\'+object_name.text+".py", 'wt', encoding='utf-8') as dest:
            dest.write("# GearEngine2D project\nfrom kivy.app import App\nfrom kivy.uix.boxlayout import BoxLayout\nfrom kivy.uix.floatlayout import FloatLayout\nfrom kivy.uix.button import Button\nfrom kivy.uix.label import Label\nfrom kivy.uix.screenmanager import ScreenManager, Screen\nfrom kivy.animation import Animation\nfrom kivy.clock import Clock\nfrom kivy.config import Config\nfrom kivy.config import Config\nfrom kivy.uix.image import Image\nfrom kivy.core import audio\nfrom kivy.core.audio import SoundLoader\nfrom kivy.uix.textinput import TextInput\nfrom kivy.core.window import Window\nWindow.clearcolor = (1, 1, 1, 1)\n#import socket\n#sock = socket.socket()\n#sock.bind(('', 9090))\n#sock.listen(1)\n \n \nConfig.set('graphics', 'resizable', '0')\nWindow.size = ("+object_width.text+","+object_height.text+")\nclass MainApp(App):\n    def build(self):\n        self.title = '"+object_name.text+"'\n        main_layout = FloatLayout()\n# CODE\n        return main_layout\n# DEFS\n \n \n \nif __name__ == '__main__':\n    app = MainApp()\n    app.run()")

    def add_textinput(self,instance):
        #messagebox.showinfo("Basic Example", "a Basic Tk MessageBox")
        #messagebox.showerror("Basic Example", "a Basic Tk MessageBox")
        #messagebox.showwarning("Basic Example", "a Basic Tk MessageBox")

        
        #from kivy.core import audio
        #sound = SoundLoader.load('mytest.wav')
        #sound.play()
        #plyer.notification.notify(message='This is not yet available in GearEngine2D', app_name='GearEngine2D', title='GearEngine2D')
        layout = BoxLayout(orientation="vertical")
        object_settings_lbl = Label(text="Object type: Sound", font_size='12sp')
        object_name_lbl = Label(text="TextInput name:", font_size='12sp')
        textinput_name = TextInput(text='name', background_normal='man3.png', font_size='12sp')
        object_text_lbl = Label(text="text:", font_size='12sp')
        object_text_textinput = TextInput(text='text', background_normal='man3.png', font_size='12sp')
        object_background_lbl = Label(text="background normal:", font_size='12sp')
        object_background_textinput = TextInput(text='C:/path/to/image.png', background_normal='man3.png', font_size='12sp')
        object_font_size_lbl = Label(text="font size:", font_size='12sp')
        object_font_size_textinput = TextInput(text='12', background_normal='man3.png', font_size='12sp')
        object_position_lbl = Label(text="position (X/Y):", font_size='12sp')
        object_positionX_textinput = TextInput(text='.5', background_normal='man3.png', font_size='12sp')
        object_positionY_textinput = TextInput(text='.5', background_normal='man3.png', font_size='12sp')
        object_size_lbl = Label(text="size (width/height):", font_size='12sp')
        object_size_width_textinput = TextInput(text='.5', background_normal='man3.png', font_size='12sp')
        object_size_height_textinput = TextInput(text='.5', background_normal='man3.png', font_size='12sp')
        button = Button(text='Create & close')
        layout.add_widget(object_settings_lbl)
        layout.add_widget(object_name_lbl)
        layout.add_widget(textinput_name)
        layout.add_widget(object_text_lbl)
        layout.add_widget(object_text_textinput)
        layout.add_widget(object_background_lbl)
        layout.add_widget(object_background_textinput)
        layout.add_widget(object_font_size_lbl)
        layout.add_widget(object_font_size_textinput)
        layout.add_widget(object_position_lbl)
        layout.add_widget(object_positionX_textinput)
        layout.add_widget(object_positionY_textinput)
        layout.add_widget(object_size_lbl)
        layout.add_widget(object_size_width_textinput)
        layout.add_widget(object_size_height_textinput)
        layout.add_widget(button)

        
        popup = Popup(title='New TextInput Property', content=layout, size_hint=(None, None), size=(700, 600))
        button.bind(on_press=partial(self.write_file_textinput, textinput_name, object_text_textinput, object_background_textinput, object_font_size_textinput, object_positionX_textinput, object_positionY_textinput, object_size_width_textinput, object_size_height_textinput))
        button.bind(on_press=popup.dismiss)
        popup.open()
        ################################################

    def write_file_textinput(self, textinput_name, object_text_textinput, object_background_textinput, object_font_size_textinput, object_positionX_textinput, object_positionY_textinput, object_size_width_textinput, object_size_height_textinput, *args):

        
       
        global FILE_NAME
        inp = askopenfile(mode="r", title="add TextInput")
        if inp is None:
            return
        FILE_NAME = inp.name
        print(FILE_NAME)
        print(inp)


        with open(FILE_NAME, 'rt', encoding='utf-8') as src:
            data = src.read()
        with open(FILE_NAME, 'wt', encoding='utf-8') as dest:
            dest.write(data.replace('# CODE', '# TextInput '+str(textinput_name.text)+'\n        '+str(textinput_name.text)+' = TextInput(text="'+str(object_text_textinput.text)+'", background_normal="'+str(object_background_textinput.text)+'", font_size="'+str(object_font_size_textinput.text)+'",'+" pos_hint = {'center_x':"+str(object_positionX_textinput.text)+", 'center_y':"+str(object_positionY_textinput.text)+"}, size_hint =("+str(object_size_width_textinput.text)+","+str(object_size_height_textinput.text)+"))\n        main_layout.add_widget("+str(textinput_name.text)+")\n# CODE"))


    def release_notes(self, instance):
        RNmsg = "- bug fixes\n- new user interface"
        messagebox.showinfo("GearEngine2D LOG", "------------------(C) Stas Povalaev------------------\n ------------------GearEngine2D------------------\n ------------------Release Notes------------------\n" + RNmsg)

    # open documentation
    def open_help(self, instance):
        os.system("documentation.txt")


    def update_engine(self, instance):
        webbrowser.open('https://www.youtube.com/channel/UCXbCn5IlqicEongzAS2s4IQ', new=2)




class ScreenTwo(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        bgImg1 = Image(source='man2.png', pos=(300,-100), color=(1,1,1, 0.5))
        self.add_widget(bgImg1)

        self.label = Label(text = "GearEngine2D | (C) Stas Povalaev | Business | v.0.0.3a", color=(.5,.5,.5, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.03})
        self.add_widget(self.label)

        self.labelAuthor = Label(text = "YouTube: Ixieane\nGameEngine for Business Use\n You can open documentation or youtube channel! ", color=(1,1,1, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.labelAuthor)

        btn2 = Button(text = "<< Back", size_hint = (.05, .05), pos_hint = {'center_x': 0.025, 'center_y': 0.97})
        btn2.bind(on_press=self.changer)
        self.add_widget(btn2)

        


        


    def changer(self,*args):
        self.manager.current = 'screen1'

    def test(self,instance):
        print('This is another test')






class ScreenPreferences(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = Label(text = "GearEngine2D | (C) Stas Povalaev | Business | v.0.0.3a", color=(.5,.5,.5, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.03})
        self.add_widget(self.label)

        self.labelAuthor = Label(text = "Preferences", color=(1,1,1, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.labelAuthor)

        btn2Back = Button(text = "<< Back", size_hint = (.05, .05), pos_hint = {'center_x': 0.025, 'center_y': 0.97})
        btn2Back.bind(on_press=self.changer)
        self.add_widget(btn2Back)


    def changer(self,*args):
        self.manager.current = 'screen1'

class ScreenZero(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = Label(text = "GearEngine2D | (C) Stas Povalaev | Business | v.0.0.3a", color=(.5,.5,.5, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.03})
        self.add_widget(self.label)
        self.labelMain = Label(text = "GearEngine2D", color=(1,1,1, 1), size_hint = (.7, .3), font_size='72sp', pos_hint = {'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(self.labelMain)

        #self.labelAuthor = Label(text = "Preferences", color=(1,1,1, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        #self.add_widget(self.labelAuthor)

        BtnNewProjectZero = Button(text = "New Project", size_hint = (.10, .10), pos_hint = {'center_x': 0.4, 'center_y': 0.5})
        BtnNewProjectZero.bind(on_press=self.changer)
        self.add_widget(BtnNewProjectZero)
        BtnLoadProjectZero = Button(text = "Load Project", size_hint = (.10, .10), pos_hint = {'center_x': 0.6, 'center_y': 0.5})
        self.add_widget(BtnLoadProjectZero)
        BtnMarketPlace = Button(text = "Marketplace", size_hint = (.10, .10), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        BtnMarketPlace.bind(on_press=self.go_to_marketplace)
        self.add_widget(BtnMarketPlace)
        BtnExitZero = Button(text = "Exit", size_hint = (.10, .10), pos_hint = {'center_x': 0.5, 'center_y': 0.4})
        BtnExitZero.bind(on_press=self.changer1)
        self.add_widget(BtnExitZero)


    def changer(self,*args):
        self.manager.current = 'screen1'
    def go_to_marketplace(self,*args):
        self.manager.current = 'screen4'

    def changer1(self,*args):
        TestApp().stop()



class ScreenMarketPlace(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = Label(text = "GearEngine2D | (C) Stas Povalaev | Business | v.0.0.3a", color=(.5,.5,.5, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.25, 'center_y': 0.03})
        self.add_widget(self.label)

        self.labelAuthor = Label(text = "MarketPlace", color=(1,1,1, 1), size_hint = (.1, .1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.labelAuthor)

        btn2Back = Button(text = "<< Back", size_hint = (.05, .05), pos_hint = {'center_x': 0.025, 'center_y': 0.97})
        btn2Back.bind(on_press=self.changer)
        self.add_widget(btn2Back)


    def changer(self,*args):
        self.manager.current = 'screen0'

class TestApp(App):

    def build(self):
        self.title = 'GearEngine2D'
        sm = ScreenManager()
        sc0 = ScreenZero(name='screen0')
        sc1 = ScreenOne(name='screen1')
        sc2 = ScreenTwo(name='screen2')
        sc3 = ScreenPreferences(name='screen3')
        sc4 = ScreenMarketPlace(name='screen4')
        sm.add_widget(sc0)
        sm.add_widget(sc1)
        sm.add_widget(sc2)
        sm.add_widget(sc3)
        sm.add_widget(sc4)
        print (sm.screen_names)
        return sm


if __name__ == '__main__':
    """
    key = input("license key: ")
    if key == "GFB2813F":
        TestApp().run()
    else:
        TestApp().stop()
    """
    TestApp().run()