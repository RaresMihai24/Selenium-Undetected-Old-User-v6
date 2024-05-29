# Selenium-Undetected-Old-User-v3

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

### Does not work if you don't have latest version of GC installed.
### Does not work with later versions of python. Python 3.9 required.

# Install
```
C:\Users\Your_user\AppData\Local\Programs\Python\Python39\python.exe -m pip install undetected_chromedriver
```

# Running
```
C:\Users\Your_user\AppData\Local\Programs\Python\Python39\python.exe C:\Users\Your_user\bot\main.py
```
