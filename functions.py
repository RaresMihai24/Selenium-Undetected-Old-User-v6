import random
import time
import requests
import logging
import psutil
import threading
import sys
import os
import undetected_chromedriver as uc
import customtkinter as ctk
from timezones import timezones
from fonts import fonts
from user_agents import *
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, DesiredCapabilities
from selenium.webdriver.common.by import By

logging.basicConfig(filename='log.txt', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

current_theme = "dark"

def get_zipcode_from_ip():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        zipcode = data.get('postal', '[ERROR]No postal code found')
        return zipcode
    except requests.RequestException as e:
        return f'[ERROR]: {e}'

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
    from gui import user_agent_var, timezone_var, font_var, web_engine_var, platform_var, browser_name_var, loc, terminal_box, progress, url_entry

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
        driver.get("https://www.x.com")

    try:
        logs = driver.get_log('performance')
        with open('performance_logs.txt', 'w') as f:
            for log in logs:
                f.write(f"{log}\n")
    except Exception as e:
        logging.error(f"Error getting performance logs: {e}")
    zipcode = get_zipcode_from_ip()
    update_message(f"Browser started\nTimezone: {timezone}\nFont: {font}\nUser Agent: {user_agent}\nURL: {url if url else 'https://www.x.com'}\nZipcode: {zipcode}\n", color="green")
    progress.stop()
    logging.info("Browser started successfully")

def terminate_browser():
    logging.info("Terminating browser...")
    terminate_chrome_processes()
    update_message("Browser terminated\n", color="red")
    logging.info("Browser terminated successfully")

def update_message(msg, color="black"):
    from gui import terminal_box
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
        from gui import glow_message_label
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

def restart_program():
    """Restart the current program."""
    python = sys.executable
    os.execv(python, ['python'] + sys.argv)
