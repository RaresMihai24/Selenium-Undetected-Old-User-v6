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
    const getContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function() {
        const context = getContext.apply(this, arguments);
        const getImageData = context.getImageData;
        context.getImageData = function() {
            const data = getImageData.apply(this, arguments);
            for (let i = 0; i < data.data.length; i += 4) {
                data.data[i] = data.data[i] ^ 10;
                data.data[i+1] = data.data[i+1] ^ 10;
                data.data[i+2] = data.data[i+2] ^ 10;
            }
            return data;
        };
        return context;
    };
    """
    driver.execute_script(script)

def get_random_language():
    languages = ['en-US', 'fr-FR', 'es-ES', 'de-DE', 'it-IT', 'pt-PT', 'ru-RU', 'ja-JP', 'ko-KR', 'zh-CN']
    return random.choice(languages)


def generate_user_agents(num_agents):
    user_agents = []
    for _ in range(num_agents):
        user_agents.append(get_random_user_agent())
    return user_agents

def generate_browser_version(browser_name):
    if browser_name.lower() in ["chrome", "brave"]:
        major_version = random.choice([80, 81, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95])
        minor_version = f"{random.randint(3000, 4000)}.{random.randint(40, 99)}"
        build_version = random.randint(100, 999)
        return f"{browser_name}/{major_version}.0.{minor_version}.{build_version}"
    elif browser_name.lower() == "firefox":
        major_version = random.choice([78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90])
        minor_version = random.randint(1, 10)
        return f"{browser_name}/{major_version}.{minor_version}"
    elif browser_name.lower() == "safari":
        major_version = random.choice([13, 14, 15])
        minor_version = random.choice([0, 1])
        patch_version = random.randint(1, 9)
        return f"Version/{major_version}.{minor_version}.{patch_version} Safari/{random.randint(600, 606)}.1.15"
    elif browser_name.lower() == "edge":
        major_version = random.choice([80, 81, 83, 85, 86, 87, 88, 89, 90, 91])
        build_version = f"{random.randint(1000, 2000)}"
        return f"Edg/{major_version}.{build_version}"
    elif browser_name.lower() == "opera":
        major_version = random.choice([66, 67, 68, 69, 70, 71, 72, 73])
        minor_version = f"{random.randint(3000, 4000)}.{random.randint(60, 99)}"
        return f"OPR/{major_version}.{minor_version}"
    else:
        return f"{browser_name}/{random.randint(1, 10)}.0.{random.randint(0, 9)}"

def get_random_user_agent():
    browser_name = random.choice(browser_names)
    browser_version = generate_browser_version(browser_name)
    platform = random.choice(platforms)
    web_engine = random.choice(web_engines)
    build_detail = random.choice(["", f"; rv:{random.randint(10, 99)}.0"])
    user_agent = f"Mozilla/5.0 ({platform}) {web_engine} {browser_name}/{browser_version}{build_detail}"
    return user_agent

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
chrome_options.add_argument("--mute-audio")
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

driver.get("https://www.x.com")
modify_canvas_fingerprint(driver)
time.sleep(1e6)
driver.close()
