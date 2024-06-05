import undetected_chromedriver as uc 
import time
from selenium.webdriver import ChromeOptions
import random
import threading
from user_agents import platforms, web_engines, browser_names
from timezones import timezones
from fonts import fonts
import psutil
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

termination_message = "Press Ctrl+C to terminate the program."
termination_message2 = "Program terminated."
randomua = "Random User Agent:"

def modify_canvas_fingerprint(driver):
    script = """
    (function() {
        const originalGetContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type) {
            const context = originalGetContext.apply(this, arguments);
            if (type === '2d') {
                const originalGetImageData = context.getImageData;
                const data = imageData.data;
                for (let i = 0; i < data.length; i += 4) {
                    data[i] ^= 10;
                    data[i + 1] ^= 10;
                    data[i + 2] ^= 10;
                }
                return imageData;
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
            print(f"Terminating Chrome process with PID {proc.info['pid']}")
            proc.terminate()

def keep_running():
    print(termination_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        terminate_chrome_processes()
        print(termination_message2)

def start_browser():
    selected_user_agent = user_agent_var.get()
    selected_timezone = timezone_var.get()
    selected_font = font_var.get()
    selected_web_engine = web_engine_var.get()
    selected_platform = platform_var.get()
    selected_browser_name = browser_name_var.get()

    user_agent = selected_user_agent if selected_user_agent != "Select User Agent" else get_random_user_agent()
    timezone = selected_timezone if selected_timezone != "Select Timezone" else random.choice(timezones)
    font = selected_font if selected_font != "Select Font" else random.choice(fonts)
    web_engine = selected_web_engine if selected_web_engine != "Select WebEngine" else random.choice(web_engines)
    platform = selected_platform if selected_platform != "Select Platform" else random.choice(platforms)
    browser_name = selected_browser_name if selected_browser_name != "Select Browser" else random.choice(browser_names)

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
    chrome_options.add_argument('--load-extension=C:\\Users\\Rares\\Desktop\\uc\\uBlock-Origin')
    chrome_options.add_argument('--load-extension=C:\\Users\\Rares\\Desktop\\uc\\WRTC')
    threading.Thread(target=keep_running, daemon=True).start()
    global driver
    driver = uc.Chrome(options=chrome_options)
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
    modify_canvas_fingerprint(driver)
    spoof_timezone(driver, timezone)
    change_fonts(driver, font)
    update_message(f"Browser started\nTimezone: {timezone}\nFont: {font}\nUser Agent: {user_agent}\nURL: {url if url else 'https://www.livejasmin.com'}\n", color="green")

def terminate_browser():
    terminate_chrome_processes()
    messagebox.showinfo("Terminated", "Chrome processes terminated.")
    update_message("Browser terminated\n", color="red")

def update_message(msg, color="black"):
    terminal_box.configure(state='normal')
    terminal_box.insert('end', msg)
    terminal_box.configure(state='disabled', text_color=color)

def glow_label():
    colors = ['#FF0000', '#FF4D4D', '#FF9999', '#FF4D4D', '#FF0000']
    current_color = 0

    def change_color():
        nonlocal current_color
        glow_message_label.configure(text_color=colors[current_color])
        current_color = (current_color + 1) % len(colors)
        glow_message_label.after(150, change_color)

    change_color()

def resize_option_menu(option_menu, width):
    option_menu.configure(width=width)

def create_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Selenium Undetected Old User V4")
    root.resizable(False, False)

    image = Image.open(r"C:\Users\Rares\Desktop\uc\img.jpg")
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    frame = ctk.CTkFrame(master=root, width=800, height=600)
    frame.pack(pady=30, padx=50, fill="both", expand=True)
    
    image_label = ctk.CTkLabel(master=frame, image=photo, text="")
    image_label.grid(row=0, column=0, columnspan=2, pady=12, padx=10)
    
    label = ctk.CTkLabel(master=frame, text="Control Panel", font=("Arial", 24))
    label.grid(row=1, column=0, columnspan=2, pady=12, padx=10)
    
    control_panel_frame = ctk.CTkFrame(master=frame)
    control_panel_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

    options_frame = ctk.CTkFrame(master=frame)
    options_frame.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
    
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
    
    global user_agent_var, timezone_var, font_var, web_engine_var, platform_var, browser_name_var
    
    user_agent_var = ctk.StringVar(value="Select User Agent")
    timezone_var = ctk.StringVar(value="Select Timezone")
    font_var = ctk.StringVar(value="Select Font")
    web_engine_var = ctk.StringVar(value="Select WebEngine")
    platform_var = ctk.StringVar(value="Select Platform")
    browser_name_var = ctk.StringVar(value="Select Browser")

    option_menu_width = 200

    user_agent_menu = ctk.CTkOptionMenu(master=options_frame, variable=user_agent_var, values=["Random"] + generate_user_agents(10), width=option_menu_width, anchor="w")
    user_agent_menu.grid(row=0, column=0, pady=12, padx=10)
    user_agent_var.trace("w", lambda *args: resize_option_menu(user_agent_menu, option_menu_width))

    timezone_menu = ctk.CTkOptionMenu(master=options_frame, variable=timezone_var, values=["Random"] + timezones, width=option_menu_width, anchor="w")
    timezone_menu.grid(row=1, column=0, pady=12, padx=10)
    timezone_var.trace("w", lambda *args: resize_option_menu(timezone_menu, option_menu_width))

    font_menu = ctk.CTkOptionMenu(master=options_frame, variable=font_var, values=["Random"] + fonts, width=option_menu_width, anchor="w")
    font_menu.grid(row=2, column=0, pady=12, padx=10)
    font_var.trace("w", lambda *args: resize_option_menu(font_menu, option_menu_width))

    web_engine_menu = ctk.CTkOptionMenu(master=options_frame, variable=web_engine_var, values=["Random"] + web_engines, width=option_menu_width, anchor="w")
    web_engine_menu.grid(row=3, column=0, pady=12, padx=10)
    web_engine_var.trace("w", lambda *args: resize_option_menu(web_engine_menu, option_menu_width))

    platform_menu = ctk.CTkOptionMenu(master=options_frame, variable=platform_var, values=["Random"] + platforms, width=option_menu_width, anchor="w")
    platform_menu.grid(row=4, column=0, pady=12, padx=10)
    platform_var.trace("w", lambda *args: resize_option_menu(platform_menu, option_menu_width))

    browser_name_menu = ctk.CTkOptionMenu(master=options_frame, variable=browser_name_var, values=["Random"] + browser_names, width=option_menu_width, anchor="w")
    browser_name_menu.grid(row=5, column=0, pady=12, padx=10)
    browser_name_var.trace("w", lambda *args: resize_option_menu(browser_name_menu, option_menu_width))
    
    start_button = ctk.CTkButton(master=control_panel_frame, text="Start Browser", command=start_browser)
    start_button.grid(row=0, column=0, pady=(12, 12), padx=10)
    global url_entry
    url_entry = ctk.CTkEntry(master=control_panel_frame, placeholder_text="Enter URL")
    url_entry.grid(row=1, column=0, pady=(5, 5), padx=10)
    terminate_button = ctk.CTkButton(master=control_panel_frame, text="Terminate Browser", command=terminate_browser)
    terminate_button.grid(row=2, column=0, pady=(5, 5), padx=10)
    
    global terminal_box
    terminal_frame = ctk.CTkFrame(master=frame, width=760, height=400)
    terminal_frame.grid(row=3, column=0, columnspan=2, pady=12, padx=10, sticky="nsew")
    terminal_box = ctk.CTkTextbox(master=terminal_frame, height=145, width=760, wrap='word')
    terminal_box.pack(pady=12, padx=10, fill="both", expand=True)
    
    global glow_message_label
    glow_message_label = ctk.CTkLabel(master=terminal_frame, text="@App made by America779\n", font=("Arial", 18))
    glow_message_label.pack(pady=12, padx=10)
    glow_label()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
