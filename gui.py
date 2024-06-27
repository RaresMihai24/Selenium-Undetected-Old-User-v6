from tkinter import ttk, Toplevel, Listbox, Scrollbar, END
import customtkinter as ctk
from functions import *
import locale_ro as loc
from PIL import Image
from timezones import timezones
from fonts import fonts
from user_agents import *

glow_message_label = None
progress = None
terminal_box = None
url_entry = None
user_agent_var = None
timezone_var = None
font_var = None
web_engine_var = None
platform_var = None
browser_name_var = None
checkbox1_var = None
checkbox2_var = None
checkbox3_var = None
checkbox4_var = None

class CustomOptionMenu(ctk.CTkFrame):
    def __init__(self, master, variable, values, width, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.variable = variable
        self.values = values
        self.width = width

        self.button = ctk.CTkButton(self, text=variable.get(), command=self.open_menu, width=width, fg_color="#007700", hover_color="#005500")
        self.button.pack(fill="both", expand=True)

        self.variable.trace("w", self.update_button_text)

    def open_menu(self):
        top = Toplevel(self)
        top.transient(self)
        top.geometry(f"{self.width}x200")

        root_x = self.winfo_rootx()
        root_y = self.winfo_rooty()
        root_width = self.winfo_width()
        root_height = self.winfo_height()

        x = root_x + (root_width // 2) - (self.width // 2)
        y = root_y + (root_height // 2) - 100
        top.geometry(f"+{x}+{y}")

        top.configure(bg='#333333')

        scrollbar = Scrollbar(top)
        scrollbar.pack(side="right", fill="y")

        listbox = Listbox(top, yscrollcommand=scrollbar.set, bg='#444444', fg='white', selectbackground='#32a852', selectforeground='black')
        for item in self.values:
            listbox.insert(END, item)
        listbox.pack(fill="both", expand=True)

        scrollbar.config(command=listbox.yview)

        listbox.bind("<<ListboxSelect>>", lambda event: self.on_select(event, listbox, top))

    def on_select(self, event, listbox, top):
        selection = listbox.get(listbox.curselection())
        self.variable.set(selection)
        top.destroy()

    def update_button_text(self, *args):
        self.button.configure(text=self.variable.get())

def create_gui():
    global glow_message_label, progress, terminal_box, url_entry, user_agent_var, timezone_var, font_var, web_engine_var, platform_var, browser_name_var, checkbox1_var, checkbox2_var, checkbox3_var, checkbox4_var
    root = ctk.CTk()
    root.title("Selenium Undetected Old User V6")
    root.resizable(False, False)

    frame = ctk.CTkFrame(master=root, width=1000, height=600)
    frame.pack(pady=60, padx=50, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text=loc.control_panel_text, font=("Arial", 24))
    label.grid(row=0, column=0, columnspan=3, pady=12, padx=10)
    
    control_panel_frame = ctk.CTkFrame(master=frame)
    control_panel_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

    options_frame = ctk.CTkFrame(master=frame)
    options_frame.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
    
    additional_frame = ctk.CTkFrame(master=frame)
    additional_frame.grid(row=1, column=2, pady=10, padx=10, sticky="nsew")

    control_panel_frame.grid_rowconfigure(0, weight=1)
    control_panel_frame.grid_rowconfigure(1, weight=1)
    control_panel_frame.grid_rowconfigure(2, weight=1)
    control_panel_frame.grid_rowconfigure(3, weight=1)
    control_panel_frame.grid_rowconfigure(4, weight=1)
    control_panel_frame.grid_columnconfigure(0, weight=1)
    
    options_frame.grid_rowconfigure(0, weight=1)
    options_frame.grid_rowconfigure(1, weight=1)
    options_frame.grid_rowconfigure(2, weight=1)
    options_frame.grid_rowconfigure(3, weight=1)
    options_frame.grid_rowconfigure(4, weight=1)
    options_frame.grid_rowconfigure(5, weight=1)
    options_frame.grid_rowconfigure(6, weight=1)
    options_frame.grid_columnconfigure(0, weight=1)
    
    additional_frame.grid_rowconfigure(0, weight=1)
    additional_frame.grid_rowconfigure(1, weight=1)
    additional_frame.grid_rowconfigure(2, weight=1)
    additional_frame.grid_rowconfigure(3, weight=1)
    additional_frame.grid_columnconfigure(0, weight=1)
    
    user_agent_var = ctk.StringVar(value=loc.select_user_agent)
    timezone_var = ctk.StringVar(value=loc.select_timezone)
    font_var = ctk.StringVar(value=loc.select_font)
    web_engine_var = ctk.StringVar(value=loc.select_web_engine)
    platform_var = ctk.StringVar(value=loc.select_platform)
    browser_name_var = ctk.StringVar(value=loc.select_browser)
    checkbox1_var = ctk.IntVar()
    checkbox2_var = ctk.IntVar()
    checkbox3_var = ctk.IntVar()
    checkbox4_var = ctk.IntVar()

    option_menu_width = 200

    timezone_menu = CustomOptionMenu(master=options_frame, variable=timezone_var, values=[loc.random_option] + timezones, width=option_menu_width)
    timezone_menu.grid(row=1, column=0, pady=12, padx=10)

    font_menu = CustomOptionMenu(master=options_frame, variable=font_var, values=[loc.random_option] + fonts, width=option_menu_width)
    font_menu.grid(row=2, column=0, pady=12, padx=10)

    web_engine_menu = CustomOptionMenu(master=options_frame, variable=web_engine_var, values=[loc.random_option] + web_engines, width=option_menu_width)
    web_engine_menu.grid(row=3, column=0, pady=12, padx=10)

    platform_menu = CustomOptionMenu(master=options_frame, variable=platform_var, values=[loc.random_option] + platforms, width=option_menu_width)
    platform_menu.grid(row=4, column=0, pady=12, padx=10)

    browser_name_menu = CustomOptionMenu(master=options_frame, variable=browser_name_var, values=[loc.random_option] + browser_names, width=option_menu_width)
    browser_name_menu.grid(row=5, column=0, pady=12, padx=10)
    
    start_button = ctk.CTkButton(master=control_panel_frame, text=loc.start_browser_text, command=start_browser_threaded, fg_color="#007700", hover_color="#005500")
    start_button.grid(row=0, column=0, pady=(12, 12), padx=10)
    url_entry = ctk.CTkEntry(master=control_panel_frame, placeholder_text=loc.enter_url_text)
    url_entry.grid(row=1, column=0, pady=(5, 5), padx=10)
    terminate_button = ctk.CTkButton(master=control_panel_frame, text=loc.terminate_browser_text, command=terminate_browser, fg_color="#007700", hover_color="#005500")
    terminate_button.grid(row=2, column=0, pady=(5, 5), padx=10)

    toggle_theme_button = ctk.CTkButton(master=control_panel_frame, text=loc.toggle_theme_text, command=toggle_theme, fg_color="#007700", hover_color="#005500")
    toggle_theme_button.grid(row=3, column=0, pady=(5, 5), padx=10)

    restart_button = ctk.CTkButton(master=control_panel_frame, text="Restart Program", command=restart_program, fg_color="#007700", hover_color="#005500")
    restart_button.grid(row=4, column=0, pady=(5, 5), padx=10)

    checkbox1 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_cookies_text, variable=checkbox1_var, fg_color="#007700", hover_color="#005500")
    checkbox1.grid(row=1, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox2 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_links_text, variable=checkbox2_var, fg_color="#007700", hover_color="#005500")
    checkbox2.grid(row=3, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox3 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_scripts_text, variable=checkbox3_var, fg_color="#007700", hover_color="#005500")
    checkbox3.grid(row=2, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox4 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_sent_data_text, variable=checkbox4_var, fg_color="#007700", hover_color="#005500")
    checkbox4.grid(row=0, column=0, pady=(12, 12), padx=10, sticky='n')
    
    terminal_frame = ctk.CTkFrame(master=frame, width=1140, height=400)
    terminal_frame.grid(row=2, column=0, columnspan=3, pady=12, padx=10, sticky="nsew")
    terminal_box = ctk.CTkTextbox(master=terminal_frame, height=145, width=1140, wrap='word')
    terminal_box.pack(pady=12, padx=10, fill="both", expand=True)
    
    glow_message_label = ctk.CTkLabel(master=terminal_frame, text=loc.all_rights_reserved_text, font=("Arial", 18))
    glow_message_label.pack(pady=12, padx=10)
    glow_label()
    
    progress_frame = ctk.CTkFrame(master=control_panel_frame)
    progress_frame.grid(row=5, column=0, pady=(5, 5), padx=10, sticky="ew")

    progress = ttk.Progressbar(master=progress_frame, orient="horizontal", mode="indeterminate", style="Custom.Horizontal.TProgressbar")
    progress.pack(fill="x", expand=True)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar",
                    thickness=5,
                    troughcolor='#2E2E2E',
                    troughrelief='flat',
                    bordercolor='#2E2E2E',
                    background='#32a852',
                    lightcolor='#32a852',
                    darkcolor='#32a852')

    root.mainloop()
