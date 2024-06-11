# Selenium-Undetected-Old-User-v5

![image](https://github.com/RaresMihai24/Selenium-Undetected-Old-User-v4/assets/126671528/a5348c0a-cdd6-457c-9a7e-b2042cc00ea5)

## v5 Update CL
- resolved warnings
- added collections for data/links/sent-data/cookies
- improved functionality
- added a toggle theme button for the people that hate their eyes
- fancier copyright

## v4 Update CL
- refactored fully the main function
- added more fonts
- separated timezones/fonts from the main
- created GUI(wip)
- added functionality to choose UA/WebEngine/Font/Timezone/Platform/Browser
- added a terminal to see the settings with which the browser started
- added a textfield for victim URL

## v3 Update CL
- refactored modify_canvas_fingerprint() to bypass newest protection
- refactored generate_user_agents() to bypass newest protection
- refactored generate_browser_version() in order to get more accurate browser versions to the reality
- refactored get_random_user_agent() to include edge cases like safari/firefox/IE
- eliminated unreadable languages from get_random_language()
- added spoof_timezone() to do inimaginable things
- added change_fonts() to do also inimaginable things
- updated WRTC
- updated uBlock-Origin

## v2 Update CL
- inject & modify getImageData & getContext
- allow js
- random language select at boot
- better generation of user agents
- fixed imp psutil
- disabled WRTC by extension 
- added uBlock Origin
- firstly boots to blank, injects the modified js, then gets to the victim

Created to bypass user recognition of some websites. Best usage and results with a premium VPN like cyberghost.

# Libraries used
- undetected chrome driver
- selenium web driver
- threading
- tkinter & customtkinter

### Required Python version: 3.9
### You need to have the last version of google chrome installed.
### You need to extract the WRTC & uBlock-Origin extensions from the google chrome store.
### You need to create the folder data/cookies.txt / data/links.txt / data/performance_logs.txt / data/scripts.txt

# Install
```
C:\Users\Your_user\AppData\Local\Programs\Python\Python39\python.exe -m pip install undetected_chromedriver
```

# Running
```
C:\Users\Your_user\AppData\Local\Programs\Python\Python39\python.exe C:\Users\Your_user\bot\main.py
```
