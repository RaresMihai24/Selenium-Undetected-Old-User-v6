import undetected_chromedriver as uc 
import time
from selenium.webdriver import ChromeOptions
import random

def generate_user_agents(num_agents):
    user_agents = []
    for _ in range(num_agents):
        user_agents.append(get_random_user_agent())
    return user_agents

def get_random_user_agent():
    platforms = [
        "Windows NT 10.0; Win64; x64",
        "Macintosh; Intel Mac OS X 10_15_7",
        "X11; Linux x86_64",
        "Windows NT 6.1; Win64; x64",
        "Windows NT 6.3; Win64; x64",
        "X11; Ubuntu; Linux x86_64",
        "X11; FreeBSD amd64",
        "Windows NT 5.1; Win64; x64",
        "Macintosh; Intel Mac OS X 10_13_6",
        "X11; Arch Linux; Linux x86_64",
        "Windows NT 6.2; Win64; x64",
        "X11; Gentoo; Linux x86_64",
        "Windows NT 6.0; Win64; x64",
        "X11; Fedora; Linux x86_64",
        "Windows NT 5.2; Win64; x64",
    ]
    
    web_engines = [
        "AppleWebKit/537.36",
        "AppleWebKit/537.36",
        "AppleWebKit/605.1.15",
        "AppleWebKit/537.36",
        "AppleWebKit/537.36",
        "AppleWebKit/537.36",
        "AppleWebKit/537.36",
        "AppleWebKit/605.1.15",
        "AppleWebKit/605.1.14",
        "AppleWebKit/605.1.13",
        "AppleWebKit/605.1.12",
        "AppleWebKit/605.1.11",
        "AppleWebKit/605.1.10",
        "AppleWebKit/605.1.9",
        "AppleWebKit/605.1.8",
        "AppleWebKit/605.1.7",
        "AppleWebKit/605.1.6",
        "AppleWebKit/605.1.5",
        "AppleWebKit/605.1.4",
        "AppleWebKit/605.1.3",
        "AppleWebKit/605.1.2",
        "AppleWebKit/605.1.1",
        "AppleWebKit/605.0.99",
        "AppleWebKit/605.0.98",
        "AppleWebKit/605.0.97",
        "AppleWebKit/605.0.96",
        "AppleWebKit/605.0.95",
        "AppleWebKit/605.0.94",
        "AppleWebKit/605.0.93",
        "AppleWebKit/605.0.92",
        "AppleWebKit/605.0.91",
        "AppleWebKit/605.0.90",
        "AppleWebKit/605.0.89",
        "AppleWebKit/605.0.88",
        "AppleWebKit/605.0.87",
        "AppleWebKit/605.0.86",
        "AppleWebKit/605.0.85",
        "AppleWebKit/605.0.84",
        "AppleWebKit/605.0.83",
        "AppleWebKit/605.0.82",
        "AppleWebKit/605.0.81",
        "AppleWebKit/605.0.80",
        "AppleWebKit/605.0.79",
        "AppleWebKit/605.0.78",
        "AppleWebKit/605.0.77",
        "AppleWebKit/605.0.76",
        "AppleWebKit/605.0.75",
        "AppleWebKit/605.0.74",
        "AppleWebKit/605.0.73",
        "AppleWebKit/605.0.72",
        "AppleWebKit/605.0.71",
        "AppleWebKit/605.0.70",
        "AppleWebKit/605.0.69",
        "AppleWebKit/605.0.68",
        "AppleWebKit/605.0.67",
        "AppleWebKit/605.0.66",
        "AppleWebKit/605.0.65",
        "AppleWebKit/605.0.64",
        "AppleWebKit/605.0.63",
        "AppleWebKit/605.0.62",
        "AppleWebKit/605.0.61",
        "AppleWebKit/605.0.60",
        "AppleWebKit/605.0.59",
        "AppleWebKit/605.0.58",
        "AppleWebKit/605.0.57",
        "AppleWebKit/605.0.56",
        "AppleWebKit/605.0.55",
        "AppleWebKit/605.0.54",
        "AppleWebKit/605.0.53",
        "AppleWebKit/605.0.52",
        "AppleWebKit/605.0.51",
        "AppleWebKit/605.0.50",
        "AppleWebKit/605.0.49",
        "AppleWebKit/605.0.48",
        "AppleWebKit/605.0.47",
        "AppleWebKit/605.0.46",
        "AppleWebKit/605.0.45",
        "AppleWebKit/605.0.44",
        "AppleWebKit/605.0.43",
        "AppleWebKit/605.0.42",
        "AppleWebKit/605.0.41",
        "AppleWebKit/605.0.40",
        "AppleWebKit/605.0.39",
        "AppleWebKit/605.0.38",
        "AppleWebKit/605.0.37",
        "AppleWebKit/605.0.36",
        "AppleWebKit/605.0.35",
        "AppleWebKit/605.0.34",
        "AppleWebKit/605.0.33",
        "AppleWebKit/605.0.32",
        "AppleWebKit/605.0.31",
        "AppleWebKit/605.0.30",
        "AppleWebKit/605.0.29",
        "AppleWebKit/605.0.28",
        "AppleWebKit/605.0.27",
        "AppleWebKit/605.0.26",
        "AppleWebKit/605.0.25",
        "AppleWebKit/605.0.24",
        "AppleWebKit/605.0.23",
        "AppleWebKit/605.0.22",
        "AppleWebKit/605.0.21",
        "AppleWebKit/605.0.20",
        "AppleWebKit/605.0.19",
        "AppleWebKit/605.0.18",
        "AppleWebKit/605.0.17",
        "AppleWebKit/605.0.16",
        "AppleWebKit/605.0.15",
        "AppleWebKit/605.0.14",
        "AppleWebKit/605.0.13",
        "AppleWebKit/605.0.12",
        "AppleWebKit/605.0.11",
        "AppleWebKit/605.0.10",
        "AppleWebKit/605.0.9",
        "AppleWebKit/605.0.8",
        "AppleWebKit/605.0.7",
        "AppleWebKit/605.0.6",
        "AppleWebKit/605.0.5",
        "AppleWebKit/605.0.4",
        "AppleWebKit/605.0.3",
        "AppleWebKit/605.0.2",
        "AppleWebKit/605.0.1",
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    ]
    
    browser_names = [
        "Chrome",
        "Firefox",
        "Safari",
        "Edge",
        "Opera",
        "Brave",
    ]
    
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

user_agents = generate_user_agents(50)

user_agent = random.choice(user_agents)
print("Random User-Agent:", user_agent)

chrome_options = ChromeOptions()

min_width, max_width = 10.00, 182.0
min_height, max_height = 50.0, 88.0
width = random.randint(min_width, max_width)
height = random.randint(min_height, max_height)

chrome_options.add_argument(f"--window-size={width},{height}")

chrome_options.add_argument(f"--user-agent={user_agent}")

driver = uc.Chrome(options=chrome_options)
driver.delete_all_cookies()
driver.execute_script("window.localStorage.clear();")
driver.execute_script("window.sessionStorage.clear();")
time.sleep(3)
driver.get("https://siteofchoice.com") 
time.sleep(108000)
driver.close()
