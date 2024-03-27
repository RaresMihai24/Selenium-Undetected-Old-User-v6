import undetected_chromedriver as uc 
import time
from selenium.webdriver import ChromeOptions
import random
import threading
from user_agents import platforms, web_engines, browser_names


termination_message = "Press Ctrl+C to terminate the program."
termination_message2 = "Program terminated."
randomua = "Random User Agent:"

def generate_user_agents(num_agents):
    user_agents = []
    for _ in range(num_agents):
        user_agents.append(get_random_user_agent())
    return user_agents

def get_random_user_agent():
    
    chrome_version = "Chrome/" + str(random.randint(80, 100)) + ".0." + str(random.randint(1000, 9999)) + "." + str(random.randint(10, 99))
    firefox_version = "Firefox/" + str(random.randint(80, 100)) + ".0"
    safari_version = "Version/" + str(random.randint(10, 15)) + ".0.2 Safari/605.1.15"
    edge_version = "Edg/" + str(random.randint(80, 100)) + ".0.1000"
    opera_version = "OPR/" + str(random.randint(80, 100)) + ".0.1000.0"
    brave_version = "Chrome/" + str(random.randint(80, 100)) + ".0." + str(random.randint(1000, 9999)) + ".110 Safari/537.36"
    
    browser_versions = [
        chrome_version,
        firefox_version,
        safari_version,
        edge_version,
        opera_version,
        brave_version,
    ]
    
    platform = random.choice(platforms)
    web_engine = random.choice(web_engines)
    browser_name = random.choice(browser_names)
    browser_version = random.choice(browser_versions)
    
    user_agent = f"Mozilla/5.0 ({platform}) {web_engine} {browser_name}/{browser_version}"
    
    return user_agent

def keep_running():
    print(termination_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        driver.close()
        driver.quit()
        print(termination_message2)

user_agents = generate_user_agents(10)

user_agent = random.choice(user_agents)
print(randomua, user_agent)

chrome_options = ChromeOptions()

min_width, max_width = 1500, 1920
min_height, max_height = 600, 1080
width = random.randint(min_width, max_width)
height = random.randint(min_height, max_height)


chrome_options.add_argument(f"--user-agent={user_agent}")

threading.Thread(target=keep_running, daemon=True).start()

driver = uc.Chrome(options=chrome_options)
driver.set_window_size(width,height)
driver.delete_all_cookies()
driver.execute_script("window.localStorage.clear();")
driver.execute_script("window.sessionStorage.clear();")
driver.get("https://www.livejasmin.com")
time.sleep(1e6)
driver.close()
