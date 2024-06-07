from tkinter import ttk, Toplevel, Listbox, Scrollbar, StringVar, END
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, DesiredCapabilities
from selenium.webdriver.common.by import By
from user_agents import platforms, web_engines, browser_names
from timezones import timezones
from fonts import fonts
import locale_ro as loc
from PIL import Image
import undetected_chromedriver as uc
import customtkinter as ctk
import time
import random
import threading
import psutil
import logging
import os

logging.basicConfig(filename='log.txt', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

current_theme = "dark"

def modify_canvas_fingerprint(driver):
    script = """
    (function() {
        const originalGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type) {
            const context = originalGetContext.apply(this, arguments);
            if (type === '2d') {
                const originalGetImageData = context.getImageData;
                context.getImageData = function(sx, sy, sw, sh) {
                    const imageData = originalGetImageData.apply(this, arguments);
                    const data = imageData.data;
                    for (let i = 0; i < data.length; i += 4) {
                        data[i] ^= 10;
                        data[i + 1] ^= 10;
                        data[i + 2] ^= 10;
                    }
                    return imageData;
                };
            }
            return context;
        };
    })();
    """
    driver.execute_script(script)

def get_random_language():
    languages = [
        'en-US', 'fr-FR', 'es-ES',
        'de-DE', 'it-IT', 'pt-PT',
        'nl-NL', 'sv-SE', 'pl-PL',
        'id-ID', 'cs-CZ', 'da-DK',
        'fi-FI', 'hu-HU', 'no-NO',
        'tr-TR', 'sk-SK', 'ca-ES'
    ]
    return random.choice(languages)

def generate_user_agents(num_agents):
    user_agents = []
    for _ in range(num_agents):
        user_agents.append(get_random_user_agent())
    return user_agents

def generate_browser_version(browser_name):
    browser_name = browser_name.lower()
    version_formats = {
        "chrome": {
            "major_versions": [80, 81, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
            "version_pattern": lambda major: f"{major}.0.{random.randint(3000, 4000)}.{random.randint(40, 99)}.{random.randint(100, 999)}"
        },
        "brave": {
            "major_versions": [80, 81, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
            "version_pattern": lambda major: f"{major}.0.{random.randint(3000, 4000)}.{random.randint(40, 99)}.{random.randint(100, 999)}"
        },
        "firefox": {
            "major_versions": [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
            "version_pattern": lambda major: f"{major}.{random.randint(1, 10)}"
        },
        "safari": {
            "major_versions": [13, 14, 15],
            "version_pattern": lambda major: f"Version/{major}.{random.choice([0, 1])}.{random.randint(1, 9)} Safari/{random.randint(600, 606)}.1.15"
        },
        "edge": {
            "major_versions": [80, 81, 83, 85, 86, 87, 88, 89, 90, 91],
            "version_pattern": lambda major: f"{major}.{random.randint(1000, 2000)}"
        },
        "opera": {
            "major_versions": [66, 67, 68, 69, 70, 71, 72, 73],
            "version_pattern": lambda major: f"{major}.{random.randint(3000, 4000)}.{random.randint(60, 99)}"
        }
    }
    default_pattern = lambda: f"{browser_name.capitalize()}/{random.randint(1, 10)}.0.{random.randint(0, 9)}"
    if browser_name in version_formats:
        browser_info = version_formats[browser_name]
        major_version = random.choice(browser_info["major_versions"])
        return f"{browser_name.capitalize()}/{browser_info['version_pattern'](major_version)}"
    else:
        return default_pattern()

def get_random_user_agent():
    browser_name = random.choice(browser_names)
    browser_version = generate_browser_version(browser_name)
    platform = random.choice(platforms)
    web_engine = random.choice(web_engines)
    build_detail = ""
    if browser_name.lower() in ["firefox", "internet explorer"]:
        build_detail = f"; rv:{random.randint(10, 99)}.0"
    if browser_name.lower() == "safari":
        user_agent = f"Mozilla/5.0 ({platform}) {web_engine} {browser_version}"
    else:
        user_agent = f"Mozilla/5.0 ({platform}) {web_engine} {browser_name}/{browser_version}{build_detail}"
    return user_agent

def spoof_timezone(driver, timezone):
    script = f"""
    Intl.DateTimeFormat.prototype.resolvedOptions = function() {{
        return {{
            timeZone: '{timezone}'
        }};
    }}
    Date.prototype.getTimezoneOffset = function() {{
        return -new Date().getTimezoneOffset();
    }};
    """
    driver.execute_script(script)

def change_fonts(driver, fonts):
    script = f"""
    const style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = 'body {{ font-family: {fonts}; }}';
    document.head.appendChild(style);
    """
    driver.execute_script(script)

def terminate_chrome_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            logging.info(f"Terminating Chrome process with PID {proc.info['pid']}")
            proc.terminate()

def keep_running():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        terminate_chrome_processes()

def start_browser_threaded():
    threading.Thread(target=start_browser).start()

def start_browser():
    logging.info("Starting browser...")
    update_message("Starting browser...\n", color="blue")
    progress.start()
    
    selected_user_agent = user_agent_var.get()
    selected_timezone = timezone_var.get()
    selected_font = font_var.get()
    selected_web_engine = web_engine_var.get()
    selected_platform = platform_var.get()
    selected_browser_name = browser_name_var.get()

    user_agent = selected_user_agent if selected_user_agent != loc.select_user_agent else get_random_user_agent()
    timezone = selected_timezone if selected_timezone != loc.select_timezone else random.choice(timezones)
    font = selected_font if selected_font != loc.select_font else random.choice(fonts)
    web_engine = selected_web_engine if selected_web_engine != loc.select_web_engine else random.choice(web_engines)
    platform = selected_platform if selected_platform != loc.select_platform else random.choice(platforms)
    browser_name = selected_browser_name if selected_browser_name != loc.select_browser else random.choice(browser_names)

    chrome_options = ChromeOptions()
    min_width, max_width = 1500, 1920
    min_height, max_height = 600, 1080
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    chrome_options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    chrome_options.add_argument(f"--lang={get_random_language()}")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument('--load-extension=' + os.getenv('UBLOCK_EXTENSION_PATH', 'C:\\Users\\Rares\\Desktop\\uc\\uBlock-Origin'))
    chrome_options.add_argument('--load-extension=' + os.getenv('WRTC_EXTENSION_PATH', 'C:\\Users\\Rares\\Desktop\\uc\\WRTC'))
    
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    threading.Thread(target=keep_running, daemon=True).start()
    global driver
    driver = uc.Chrome(options=chrome_options, desired_capabilities=caps)
    driver.set_window_size(width, height)
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.get("about:blank")
    modify_canvas_fingerprint(driver)
    spoof_timezone(driver, timezone)
    change_fonts(driver, font)
    url = url_entry.get()
    if url:
        driver.get(url)
    else:
        driver.get("https://www.google.com")

    try:
        logs = driver.get_log('performance')
        with open('performance_logs.txt', 'w') as f:
            for log in logs:
                f.write(f"{log}\n")
    except Exception as e:
        logging.error(f"Error getting performance logs: {e}")

    update_message(f"Browser started\nTimezone: {timezone}\nFont: {font}\nUser Agent: {user_agent}\nURL: {url if url else 'https://www.livejasmin.com'}\n", color="green")
    progress.stop()
    logging.info("Browser started successfully")

def terminate_browser():
    logging.info("Terminating browser...")
    terminate_chrome_processes()
    update_message("Browser terminated\n", color="red")
    logging.info("Browser terminated successfully")

def update_message(msg, color="black"):
    terminal_box.configure(state='normal')
    terminal_box.insert('end', msg)
    terminal_box.configure(state='disabled', text_color=color)

def glow_label():
    colors = [
        '#00FF00', '#02FF02', '#04FF04', '#06FF06', '#08FF08', 
        '#0AFF0A', '#0CFF0C', '#0EFF0E', '#10FF10', '#12FF12', 
        '#14FF14', '#16FF16', '#18FF18', '#1AFF1A', '#1CFF1C', 
        '#1EFF1E', '#20FF20', '#22FF22', '#24FF24', '#26FF26', 
        '#28FF28', '#2AFF2A', '#2CFF2C', '#2EFF2E', '#30FF30', 
        '#32FF32', '#34FF34', '#36FF36', '#38FF38', '#3AFF3A', 
        '#3CFF3C', '#3EFF3E', '#40FF40', '#42FF42', '#44FF44', 
        '#46FF46', '#48FF48', '#4AFF4A', '#4CFF4C', '#4EFF4E', 
        '#50FF50', '#52FF52', '#54FF54', '#56FF56', '#58FF58', 
        '#5AFF5A', '#5CFF5C', '#5EFF5E', '#60FF60', '#62FF62', 
        '#64FF64', '#66FF66', '#68FF68', '#6AFF6A', '#6CFF6C', 
        '#6EFF6E', '#70FF70', '#72FF72', '#74FF74', '#76FF76', 
        '#78FF78', '#7AFF7A', '#7CFF7C', '#7EFF7E', '#80FF80', 
        '#82FF82', '#84FF84', '#86FF86', '#88FF88', '#8AFF8A', 
        '#8CFF8C', '#8EFF8E', '#90FF90', '#92FF92', '#94FF94', 
        '#96FF96', '#98FF98', '#9AFF9A', '#9CFF9C', '#9EFF9E'
    ]
    current_color = 0

    def change_color():
        nonlocal current_color
        glow_message_label.configure(text_color=colors[current_color])
        current_color = (current_color + 1) % len(colors)
        glow_message_label.after(100, change_color)

    change_color()

def resize_option_menu(option_menu, width):
    option_menu.configure(width=width)

def toggle_theme():
    global current_theme
    if current_theme == "dark":
        ctk.set_appearance_mode("light")
        current_theme = "light"
    else:
        ctk.set_appearance_mode("dark")
        current_theme = "dark"

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

def collect_cookies(driver):
    cookies = driver.get_cookies()
    with open(r'C:\Users\Rares\Desktop\uc\data\cookies.txt', 'w') as f:
        for cookie in cookies:
            f.write(f"{cookie}\n")

def collect_links(driver):
    with open(r'C:\Users\Rares\Desktop\uc\data\links.txt', 'w') as f:
        try:
            links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            for link in links:
                retry_count = 3
                while retry_count > 0:
                    try:
                        href = link.get_attribute('href')
                        if href and "http" in href:
                            f.write(f"{href}\n")
                        break
                    except StaleElementReferenceException:
                        retry_count -= 1
                        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        except Exception as e:
            logging.error(f"Error collecting links: {e}")

def collect_scripts(driver):
    with open(r'C:\Users\Rares\Desktop\uc\data\scripts.txt', 'w') as f:
        try:
            scripts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'script')))
            for script in scripts:
                retry_count = 3
                while retry_count > 0:
                    try:
                        src = script.get_attribute('src')
                        if src and "http" in src:
                            f.write(f"{src}\n")
                        break
                    except StaleElementReferenceException:
                        retry_count -= 1
                        script = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'script')))
        except Exception as e:
            logging.error(f"Error collecting scripts: {e}")

def collect_sent_data(driver):
    logs = driver.get_log('performance')
    with open(r'C:\Users\Rares\Desktop\uc\data\sent_data.txt', 'w') as f:
        for log in logs:
            f.write(f"{log}\n")

def create_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Selenium Undetected Old User V4")
    root.resizable(False, False)

    image_path = r"C:\Users\Rares\Desktop\uc\img.jpg"
    ctk_image = ctk.CTkImage(light_image=Image.open(image_path),
                                  dark_image=Image.open(image_path),
                                  size=(300, 300))

    frame = ctk.CTkFrame(master=root, width=1000, height=600)
    frame.pack(pady=30, padx=50, fill="both", expand=True)
    
    toggle_theme_button = ctk.CTkButton(master=root, text=loc.toggle_theme_text, command=toggle_theme, fg_color="#007700", hover_color="#005500")
    toggle_theme_button.place(relx=0.07, rely=0.045, anchor='nw')

    image_label = ctk.CTkLabel(master=frame, image=ctk_image, text="")
    image_label.grid(row=0, column=0, columnspan=3, pady=12, padx=10)
    
    label = ctk.CTkLabel(master=frame, text=loc.control_panel_text, font=("Arial", 24))
    label.grid(row=1, column=0, columnspan=3, pady=12, padx=10)
    
    control_panel_frame = ctk.CTkFrame(master=frame)
    control_panel_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

    options_frame = ctk.CTkFrame(master=frame)
    options_frame.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
    
    additional_frame = ctk.CTkFrame(master=frame)
    additional_frame.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")

    control_panel_frame.grid_rowconfigure(0, weight=1)
    control_panel_frame.grid_rowconfigure(1, weight=1)
    control_panel_frame.grid_rowconfigure(2, weight=1)
    control_panel_frame.grid_rowconfigure(3, weight=1)
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
    
    global user_agent_var, timezone_var, font_var, web_engine_var, platform_var, browser_name_var, checkbox1_var, checkbox2_var, checkbox3_var, checkbox4_var
    
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
    global url_entry
    url_entry = ctk.CTkEntry(master=control_panel_frame, placeholder_text=loc.enter_url_text)
    url_entry.grid(row=1, column=0, pady=(5, 5), padx=10)
    terminate_button = ctk.CTkButton(master=control_panel_frame, text=loc.terminate_browser_text, command=terminate_browser, fg_color="#007700", hover_color="#005500")
    terminate_button.grid(row=2, column=0, pady=(5, 5), padx=10)

    checkbox1 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_cookies_text, variable=checkbox1_var, fg_color="#007700", hover_color="#005500")
    checkbox1.grid(row=1, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox2 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_links_text, variable=checkbox2_var, fg_color="#007700", hover_color="#005500")
    checkbox2.grid(row=3, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox3 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_scripts_text, variable=checkbox3_var, fg_color="#007700", hover_color="#005500")
    checkbox3.grid(row=2, column=0, pady=(12, 12), padx=10, sticky='n')
    checkbox4 = ctk.CTkCheckBox(master=additional_frame, text=loc.collect_sent_data_text, variable=checkbox4_var, fg_color="#007700", hover_color="#005500")
    checkbox4.grid(row=0, column=0, pady=(12, 12), padx=10, sticky='n')
    
    global terminal_box
    terminal_frame = ctk.CTkFrame(master=frame, width=1140, height=400)
    terminal_frame.grid(row=3, column=0, columnspan=3, pady=12, padx=10, sticky="nsew")
    terminal_box = ctk.CTkTextbox(master=terminal_frame, height=145, width=1140, wrap='word')
    terminal_box.pack(pady=12, padx=10, fill="both", expand=True)
    
    global glow_message_label
    glow_message_label = ctk.CTkLabel(master=terminal_frame, text=loc.all_rights_reserved_text, font=("Arial", 18))
    glow_message_label.pack(pady=12, padx=10)
    glow_label()
    
    global progress
    progress_frame = ctk.CTkFrame(master=control_panel_frame)
    progress_frame.grid(row=3, column=0, pady=(5, 5), padx=10, sticky="ew")

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

if __name__ == "__main__":
    create_gui()
