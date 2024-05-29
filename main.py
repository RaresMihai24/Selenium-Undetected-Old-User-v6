import undetected_chromedriver as uc 
import time
from selenium.webdriver import ChromeOptions
import random
import threading
from user_agents import platforms, web_engines, browser_names
import psutil

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
                context.getImageData = function(x, y, width, height) {
                    const imageData = originalGetImageData.apply(this, arguments);
                    const data = imageData.data;
                    for (let i = 0; i < data.length; i += 4) {
                        data[i] ^= 10;     // Red channel
                        data[i + 1] ^= 10; // Green channel
                        data[i + 2] ^= 10; // Blue channel
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

user_agents = generate_user_agents(10)

user_agent = random.choice(user_agents)
print(randomua, user_agent)

language = get_random_language()
timezone = random.choice(['America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney'])
fonts = random.choice(['Arial, sans-serif', 'Verdana, sans-serif', 'Times New Roman, serif'])

chrome_options = ChromeOptions()

min_width, max_width = 1500, 1920
min_height, max_height = 600, 1080
width = random.randint(min_width, max_width)
height = random.randint(min_height, max_height)

chrome_options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
#chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument(f"--lang={language}")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
#chrome_options.add_argument("--mute-audio")
chrome_options.add_argument(f"--user-agent={user_agent}")
chrome_options.add_argument('--load-extension=C:\\Users\Rares\\Desktop\\uc\\uBlock-Origin')
chrome_options.add_argument('--load-extension=C:\\Users\Rares\\Desktop\\uc\\WRTC')

threading.Thread(target=keep_running, daemon=True).start()


driver = uc.Chrome(options=chrome_options)
driver.set_window_size(width,height)
driver.delete_all_cookies()
driver.execute_script("window.localStorage.clear();")
driver.execute_script("window.sessionStorage.clear();")
driver.get("about:blank")
modify_canvas_fingerprint(driver)
spoof_timezone(driver, timezone)
change_fonts(driver, fonts)

driver.get("https://www.x.com")
modify_canvas_fingerprint(driver)
spoof_timezone(driver, timezone)
change_fonts(driver, fonts)
time.sleep(1e6)
driver.close()
